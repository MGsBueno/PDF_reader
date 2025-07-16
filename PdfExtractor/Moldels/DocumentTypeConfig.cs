using System.Collections.Generic;
using System.Text.Json.Serialization;


namespace PdfExtractor.Models
{
    public class DocumentTypeConfig
    {
        [JsonPropertyName("blocos")]
        public Dictionary<string, BlockConfig> Blocos { get; set; } = new();

        [JsonPropertyName("ignorar")]
        public List<string> Ignorar { get; set; } = new();
    }

    
}
