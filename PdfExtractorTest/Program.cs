using System;
using System.Collections.Generic;
using System.IO;
using PdfExtractor.Models;
using PdfExtractor.Services;

class Program
{
    static void Main()
    {
        var configEditor = new ConfigEditor();

        // Define o nome do documento (chave do JSON)
        string docTypeKey = "ODS";

        // Define os blocos que deseja criar
        var blocos = new List<string> { "ODS", "Meta Global", "Meta Municipal", "Indicadores" };
        configEditor.InitConfig(docTypeKey, blocos);

        // Define os termos a ignorar
        var ignorar = new List<string>
        {
            "Página",
            "Agenda Municipal 2030",
            "Prefeitura de São Paulo",
            "Contextualização",
            "Desafios remanescentes"
        };
        configEditor.AddIgnore(docTypeKey, ignorar);

        // Garante que a pasta config exista
        Directory.CreateDirectory("config");

        // Salva o JSON em arquivo (em pasta config)
        string configPath = "config/doc_types.json";
        configEditor.Save(configPath);

        Console.WriteLine($"Configuração salva em '{configPath}'\n");

        // --- Agora carrega a configuração e processa o PDF ---

        if (!File.Exists(configPath))
        {
            Console.WriteLine($"Arquivo de configuração '{configPath}' não encontrado. Verifique se o arquivo foi criado corretamente.");
            return;
        }

        var loader = new ConfigLoader();
        DocumentTypeConfig config;

        try
        {
            config = loader.Load(configPath, docTypeKey);
            Console.WriteLine($"Configuração para '{docTypeKey}' carregada com sucesso.\n");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Erro ao carregar configuração: {ex.Message}");
            return;
        }

        // Exibir os blocos e seus padrões para ajudar na depuração
        Console.WriteLine("Blocos e seus padrões de busca:");
        foreach (var bloco in config.Blocos)
        {
            Console.WriteLine($"- Bloco: {bloco.Key}");
            if (bloco.Value.Match != null)
            {
                foreach (var pattern in bloco.Value.Match)
                {
                    Console.WriteLine($"    Padrão: {pattern}");
                }
            }
            else
            {
                Console.WriteLine("    Sem padrões (match) definidos.");
            }
        }
        Console.WriteLine();

        string pdfPath = "input/AgendaMunicipal2030_ComissaoMunicipalODS_08_07_2021_6MB.pdf";
        if (!File.Exists(pdfPath))
        {
            Console.WriteLine($"Arquivo PDF '{pdfPath}' não encontrado. Certifique-se que o arquivo está no local correto.");
            return;
        }

        var processor = new PdfProcessor(config);

        Console.WriteLine("Iniciando extração do PDF...");
        var resultados = processor.Extract(pdfPath);

        Console.WriteLine($"\nForam extraídas {resultados.Count} estruturas do PDF.");

        if (resultados.Count == 0)
        {
            Console.WriteLine("Nenhuma estrutura extraída. Verifique os padrões e o conteúdo do PDF.");
        }

        // Imprime somente os blocos extraídos para debug
        foreach (var estrutura in resultados)
        {
            if (estrutura.Blocos.Count == 0)
            {
                Console.WriteLine($"[AVISO] Estrutura '{estrutura.Titulo}' não possui blocos extraídos.");
            }
            else
            {
                foreach (var bloco in estrutura.Blocos)
                {
                    Console.WriteLine($"Bloco: {bloco.Tipo} - {bloco.Titulo}");
                    Console.WriteLine($"Texto: {bloco.Texto}\n");
                }
            }
        }

        // Garante que a pasta output exista
        string outputDir = Path.Combine("output", docTypeKey);
        Directory.CreateDirectory(outputDir);

        JsonSaver.Save(resultados, outputDir);
        Console.WriteLine($"\nResultados salvos em: {outputDir}");
    }
}
