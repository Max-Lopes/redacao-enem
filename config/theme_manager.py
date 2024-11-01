import random

class ThemeManager:
    # Lista de temas pré-definidos
    DEFAULT_THEMES = [
        "O impacto das redes sociais nas relações interpessoais no Brasil",
        "Desafios para a implementação da economia circular no contexto brasileiro",
        "A questão do acesso à educação digital no Brasil contemporâneo",
        "Caminhos para combater a desinformação na era digital",
        "O papel da tecnologia na democratização do conhecimento",
        "Desafios da mobilidade urbana nas grandes cidades brasileiras",
        "A importância da preservação ambiental para o desenvolvimento sustentável",
        "O impacto da inteligência artificial no mercado de trabalho brasileiro",
        "Desafios para a segurança alimentar no Brasil",
        "A questão da saúde mental na sociedade contemporânea",
        "O papel das redes sociais na formação da opinião pública",
        "Desafios para a promoção de políticas de saúde mental no Brasil",
        "A importância da diversidade étnica e cultural no mercado de trabalho",
        "Impactos da desinformação na sociedade brasileira",
        "O combate ao racismo estrutural no Brasil",
        "Avanços e retrocessos na igualdade de gênero no Brasil",
        "Desafios da educação digital em áreas rurais brasileiras",
        "O impacto da tecnologia no mercado de trabalho",
        "Caminhos para a inclusão de pessoas com deficiência na educação brasileira",
        "Violência contra mulheres e a importância de políticas públicas de proteção",
        "Consequências do desmatamento para a biodiversidade",
        "O papel da educação ambiental no combate às mudanças climáticas",
        "Mobilidade urbana e seus impactos na qualidade de vida",
        "Impacto das fake news no processo eleitoral brasileiro",
        "A importância da acessibilidade em espaços públicos",
        "Desafios da democratização do acesso ao ensino superior no Brasil",
        "A influência da indústria cultural na identidade brasileira",
        "Desafios para o desenvolvimento sustentável nas grandes cidades",
        "Impactos da globalização nas culturas locais",
        "Desigualdade social e a concentração de renda no Brasil",
        "A importância da preservação da Amazônia para o mundo",
        "Desafios para a segurança alimentar no Brasil",
        "O papel da ciência no combate a pandemias",
        "Desafios do sistema penitenciário brasileiro para a reintegração social",
        "Envelhecimento da população e o impacto nas políticas públicas de saúde",
        "A importância do combate ao trabalho infantil no Brasil",
        "Iniciativas para combater a evasão escolar no ensino médio brasileiro",
        "A valorização do trabalho artístico e cultural no Brasil",
        "O papel da educação na construção de uma sociedade mais inclusiva",
        "Impactos da violência urbana na vida dos jovens brasileiros",
        "A importância das campanhas de vacinação para a saúde pública",
        "O papel da educação financeira na vida dos jovens",
        "Desafios para a erradicação da pobreza no Brasil",
        "A proteção dos direitos das populações indígenas no Brasil",
        "Consequências da dependência tecnológica na vida cotidiana",
        "O impacto das queimadas na agricultura brasileira",
        "A influência da publicidade no consumo infantil",
        "O papel do esporte na promoção da cidadania",
        "A importância da preservação do patrimônio histórico brasileiro",
        "Os desafios da segurança pública e o papel da polícia comunitária",
        "Impactos dos transtornos de ansiedade na juventude",
        "A importância do voluntariado na sociedade brasileira",
        "A questão da violência no ambiente escolar",
        "O papel do jovem na construção de uma sociedade mais justa",
        "A crise habitacional e o déficit de moradias no Brasil",
        "A proteção dos animais e os desafios da conscientização ambiental",
        "A importância da liberdade de imprensa na democracia",
        "Desafios da prevenção de doenças sexualmente transmissíveis entre jovens",
        "Consequências sociais da obesidade infantil no Brasil",
        "O papel da leitura no desenvolvimento da cidadania",
        "Os impactos da imigração na sociedade brasileira"
    ]

    @staticmethod
    def get_random_theme():
        """Retorna um tema aleatório da lista de temas pré-definidos"""
        return random.choice(ThemeManager.DEFAULT_THEMES)

    @staticmethod
    def process_theme_request(form_data):
        """
        Processa a solicitação de tema do formulário
        
        Args:
            form_data: Dados do formulário enviado
            
        Returns:
            str: Tema selecionado ou gerado
        """
        print("\n=== DEBUG ThemeManager ===")
        print("Dados recebidos no form_data:", dict(form_data))
        print("Tipo de tema recebido:", form_data.get('themeOption'))
        print("Tema personalizado recebido:", form_data.get('customTema'))
        print("========================\n")
        
        tema_option = form_data.get('themeOption', '')
        
        if tema_option == 'custom':
            # Se foi selecionado tema personalizado, usa o tema digitado
            custom_tema = form_data.get('customTema', '').strip()
            if custom_tema:
                return custom_tema
            else:
                raise ValueError("Tema personalizado não pode estar vazio")
                
        elif tema_option == 'random':
            # Se foi selecionado tema aleatório, gera um tema
            return ThemeManager.get_random_theme()
            
        else:
            raise ValueError("Opção de tema inválida")