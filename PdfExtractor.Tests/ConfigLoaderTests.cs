using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using PdfExtractor.Models;
using PdfExtractor.Services;
using Xunit;

public class ConfigLoaderTests
{
    private const string JsonExample = @"
    {
        ""ODS"": {
            ""blocos"": {
                ""Bloco1"": {
                    ""match"": [""^ods""],
                    ""fim_ao_encontrar"": [""meta global""]
                },
                ""Bloco2"": {
                    ""match"": [""meta global""]
                }
            },
            ""ignorar"": [""Página"", ""Prefeitura""]
        }
    }";

    private string SaveTempJsonFile(string content)
    {
        string tempFile = Path.GetTempFileName();
        File.WriteAllText(tempFile, content);
        return tempFile;
    }

    [Fact]
    public void Load_ValidJson_ShouldLoadConfigAndPrecompileRegex()
    {
        // Arrange
        string tempFile = SaveTempJsonFile(JsonExample);
        var loader = new ConfigLoader();

        // Act
        DocumentTypeConfig config = loader.Load(tempFile, "ODS");

        // Assert
        Assert.NotNull(config);
        Assert.True(config.Blocos.ContainsKey("Bloco1"));
        Assert.True(config.Blocos.ContainsKey("Bloco2"));

        // Regex pré compilado e ignorar
        Assert.NotNull(config.Blocos["Bloco1"].CompiledPatterns);
        Assert.NotEmpty(config.Blocos["Bloco1"].CompiledPatterns);

        // RegexOptions.IgnoreCase foi usado? Testa matching case insensitive
        var regex = config.Blocos["Bloco1"].CompiledPatterns[0];
        Assert.Matches(regex,"ODS"); // maiúsculo
        Assert.Matches(regex,"ods"); // minúsculo
        Assert.Matches(regex,"OdS"); // misto

        // FimAoEncontrar deve estar normalizado para minúsculas
        var fimAoEncontrar = config.Blocos["Bloco1"].FimAoEncontrar;
        Assert.Contains("fim1", fimAoEncontrar);
        Assert.Contains("fim2", fimAoEncontrar);

        // Ignorar carregado
        Assert.Contains("Página", config.Ignorar);
        Assert.Contains("Prefeitura", config.Ignorar);

        // Cleanup
        File.Delete(tempFile);
    }

    [Fact]
    public void Load_NonExistentFile_ShouldThrowFileNotFound()
    {
        var loader = new ConfigLoader();
        Assert.Throws<FileNotFoundException>(() => loader.Load("arquivo_que_nao_existe.json", "ODS"));
    }

    [Fact]
    public void Load_MissingDocType_ShouldThrowInvalidOperation()
    {
        string tempFile = SaveTempJsonFile(JsonExample);
        var loader = new ConfigLoader();

        Assert.Throws<InvalidOperationException>(() => loader.Load(tempFile, "CHAVE_INEXISTENTE"));

        File.Delete(tempFile);
    }
}
