using System.Collections.Generic;
using PdfExtractor.Models;
using PdfExtractor.Services;
using Xunit;

public class PdfProcessorTests
{
    [Fact]
    public void Extract_ShouldReturnExpectedStructures_WithCompleteConfig()
    {
        // Montar a configuração do tipo de documento manualmente
        var config = new DocumentTypeConfig
        {
            Ignorar = new List<string>
            {
                "Página",
                "Agenda Municipal 2030",
                "Prefeitura de São Paulo",
                "Contextualização",
                "Desafios remanescentes"
            },
            Blocos = new Dictionary<string, BlockConfig>
            {
                ["ODS"] = new BlockConfig
                {
                    Match = new List<string> { "^ods" },
                    IniciaEstrutura = true,
                    DescricaoFonteMinima = 0,
                    UsaDescricao = false,
                    FimAoEncontrar = new List<string>()
                },
                ["Meta Global"] = new BlockConfig
                {
                    Match = new List<string> { "^meta global" },
                    DescricaoFonteMinima = 0
                },
                ["Meta Municipal"] = new BlockConfig
                {
                    Match = new List<string> { "^meta municipal" },
                    DescricaoFonteMinima = 0
                },
                ["Indicadores"] = new BlockConfig
                {
                    Match = new List<string> { "^indicadores" },
                    DescricaoFonteMinima = 0
                }
            }
        };

        // Importante: pré-compilar os regex das configurações para o PdfProcessor usar
        var loader = new ConfigLoader();
        loader.PrecompileRegex(config);

        var processor = new PdfProcessor(config);

        string pdfPath = "input/AgendaMunicipal2030_ComissaoMunicipalODS_08_07_2021_6MB.pdf";

        // Extrai as estruturas do PDF
        var resultados = processor.Extract(pdfPath);

        Assert.NotNull(resultados);
        Assert.NotEmpty(resultados);

        // Você pode validar mais detalhes aqui conforme conteúdo esperado
    }
}
