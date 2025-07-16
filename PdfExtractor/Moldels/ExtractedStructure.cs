using System.Collections.Generic;

namespace PdfExtractor.Models;

public class ExtractedStructure
{
    public string Titulo { get; set; } = "";
    public string Descricao { get; set; } = "";
    public List<ExtractedBlock> Blocos { get; set; } = new();
}
