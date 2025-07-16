using System.Collections.Generic;
using System.IO;
using PdfExtractor.Services;
using Xunit;

public class ConfigEditorTests
{
    [Fact]
    public void InitConfig_ShouldInitializeDocumentTypeConfig()
    {
        var editor = new ConfigEditor();
        string docTypeKey = "TESTE";
        var blocos = new List<string> { "BlocoA", "BlocoB" };

        editor.InitConfig(docTypeKey, blocos);

        // Salvar para testar se gera JSON válido
        string tempFile = Path.GetTempFileName();
        editor.Save(tempFile);

        string content = File.ReadAllText(tempFile);
        Assert.Contains(docTypeKey, content);
        Assert.Contains("BlocoA", content);
        Assert.Contains("BlocoB", content);

        File.Delete(tempFile);
    }

    [Fact]
    public void AddIgnore_ShouldAddIgnoreTerms()
    {
        var editor = new ConfigEditor();
        string docTypeKey = "TESTE";
        editor.InitConfig(docTypeKey, new List<string>());

        var ignorar = new List<string> { "Termo1", "Termo2" };
        editor.AddIgnore(docTypeKey, ignorar);

        string tempFile = Path.GetTempFileName();
        editor.Save(tempFile);

        string content = File.ReadAllText(tempFile);
        Assert.Contains("Termo1", content);
        Assert.Contains("Termo2", content);

        File.Delete(tempFile);
    }
}
