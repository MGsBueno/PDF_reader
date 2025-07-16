using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Text.Json.Serialization;

namespace PdfExtractor.Models
{
    public class BlockConfig
    {
        [JsonPropertyName("match")]
        public List<string> Match { get; set; } = new();

        [JsonPropertyName("fonte_minima")]
        public int FonteMinima { get; set; } = 0;

        [JsonPropertyName("descricao_fonte_minima")]
        public int DescricaoFonteMinima { get; set; } = 0;

        [JsonPropertyName("inicia_estrutura")]
        public bool IniciaEstrutura { get; set; } = false;

        [JsonPropertyName("usa_descricao")]
        public bool UsaDescricao { get; set; } = false;

        [JsonPropertyName("fim_ao_encontrar")]
        public List<string> FimAoEncontrar { get; set; } = new();

        // Não serialize (não é parte do JSON de configuração)
        [JsonIgnore]
        public List<System.Text.RegularExpressions.Regex> CompiledPatterns { get; set; } = new();
    }
}
