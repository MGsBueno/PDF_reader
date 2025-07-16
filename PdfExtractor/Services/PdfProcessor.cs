using System;
using System.Collections.Generic;
using System.Linq;
using PdfExtractor.Models;
using UglyToad.PdfPig;

namespace PdfExtractor.Services
{
    public class PdfProcessor
    {
        private readonly DocumentTypeConfig _docTypeConfig;
        private readonly BlockDetector _blockDetector;

        public PdfProcessor(DocumentTypeConfig docTypeConfig)
        {
            _docTypeConfig = docTypeConfig;
            _blockDetector = new BlockDetector(_docTypeConfig);
        }

        public List<ExtractedStructure> Extract(string pdfPath)
        {
            var resultadoFinal = new List<ExtractedStructure>();

            ExtractedStructure? estruturaAtual = null;
            ExtractedBlock? blocoAtual = null;
            string textoAcumulado = "";
            string? tipoAtual = null;

            using var doc = PdfDocument.Open(pdfPath);

            foreach (var pagina in doc.GetPages())
            {
                // Agrupa palavras por linha (aproximando pela coordenada Y)
                var linhas = pagina.GetWords()
                    .GroupBy(w => Math.Round(w.BoundingBox.Bottom, 0)) // ajustar a precisão se precisar
                    .OrderByDescending(g => g.Key); // topo da página para baixo

                foreach (var grupoLinha in linhas)
                {
                    string linhaTexto = string.Join(" ", grupoLinha.Select(w => w.Text)).Trim();

                    if (string.IsNullOrEmpty(linhaTexto) || _docTypeConfig.Ignorar.Contains(linhaTexto))
                        continue;

                    double fonteMedia = grupoLinha
                        .SelectMany(w => w.Letters)
                        .DefaultIfEmpty()
                        .Average(l => l?.FontSize ?? 0);

                    var nomeBloco = _blockDetector.DetectarBloco(linhaTexto.ToLower(), fonteMedia);

                    if (nomeBloco != null)
                    {
                        var regras = _docTypeConfig.Blocos[nomeBloco];

                        // Finalizar bloco atual
                        if (blocoAtual != null)
                        {
                            blocoAtual.Texto = textoAcumulado.Trim();
                            estruturaAtual?.Blocos.Add(blocoAtual);
                            blocoAtual = null;
                            textoAcumulado = "";
                        }

                        // Se inicia estrutura, finaliza estrutura anterior
                        if (regras.IniciaEstrutura)
                        {
                            if (estruturaAtual != null)
                                resultadoFinal.Add(estruturaAtual);

                            estruturaAtual = new ExtractedStructure
                            {
                                Titulo = linhaTexto,
                                Descricao = "",
                                Blocos = new List<ExtractedBlock>()
                            };
                            tipoAtual = nomeBloco;
                            continue;
                        }

                        blocoAtual = new ExtractedBlock
                        {
                            Tipo = nomeBloco,
                            Titulo = linhaTexto,
                            Texto = ""
                        };
                        tipoAtual = nomeBloco;
                        textoAcumulado = "";
                        continue;
                    }

                    // Acumular descrição ou texto do bloco
                    if (tipoAtual != null && _docTypeConfig.Blocos.TryGetValue(tipoAtual, out var regrasBloco))
                    {
                        if (regrasBloco.UsaDescricao && fonteMedia < regrasBloco.DescricaoFonteMinima)
                        {
                            // Fonte menor -> acumula em descrição
                            estruturaAtual!.Descricao += " " + linhaTexto;
                            continue;
                        }

                        // Verifica fim do bloco
                        if (regrasBloco.FimAoEncontrar != null)
                        {
                            bool encontrouFim = false;
                            foreach (var fim in regrasBloco.FimAoEncontrar)
                            {
                                if (linhaTexto.StartsWith(fim, StringComparison.OrdinalIgnoreCase))
                                {
                                    blocoAtual!.Texto = textoAcumulado.Trim();
                                    estruturaAtual!.Blocos.Add(blocoAtual);
                                    blocoAtual = null;
                                    tipoAtual = null;
                                    textoAcumulado = "";
                                    encontrouFim = true;
                                    break;
                                }
                            }
                            if (encontrouFim)
                                continue;
                        }

                        textoAcumulado += " " + linhaTexto;
                    }
                }
            }

            // Finaliza última estrutura e bloco
            if (estruturaAtual != null)
            {
                if (blocoAtual != null)
                {
                    blocoAtual.Texto = textoAcumulado.Trim();
                    estruturaAtual.Blocos.Add(blocoAtual);
                }
                resultadoFinal.Add(estruturaAtual);
            }

            return resultadoFinal;
        }
    }
}
