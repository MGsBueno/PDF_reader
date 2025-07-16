using System.Collections.Generic;
using System.IO;
using PdfExtractor.Models;
using PdfExtractor.Services;
using Xunit;

public class JsonSaverTests
{
    [Fact]
    public void Save_ShouldCreateJsonFile()
    {
        var sampleList = new List<ExtractedStructure>
        {
            new ExtractedStructure
            {
                Titulo = "Teste",
                Descricao = "Descrição de teste",
                Blocos = new List<ExtractedBlock>
                {
                    new ExtractedBlock { Tipo = "Tipo1", Titulo = "Titulo1", Texto = "Texto1" }
                }
            }
        };

        string tempDir = Path.Combine(Path.GetTempPath(), Path.GetRandomFileName());
        Directory.CreateDirectory(tempDir);

        JsonSaver.Save(sampleList, tempDir);

        string[] files = Directory.GetFiles(tempDir, "*.json");
        Assert.NotEmpty(files);

        string jsonContent = File.ReadAllText(files[0]);
        Assert.Contains("Teste", jsonContent);

        Directory.Delete(tempDir, true);
    }
}
