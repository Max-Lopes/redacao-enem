from crewai import Task
from textwrap import dedent

class ReviewTasks:
    @staticmethod
    def create_review_tasks(agents, texto, tema):
        expected_output = """{
            "nota": número entre 0 e 200,
            "justificativa": "explicação detalhada da nota",
            "problemas": ["problema 1", "problema 2"],
            "sugestoes": ["sugestão 1", "sugestão 2"]
        }"""
        
        tasks = []
        
        # Competência 1 - Língua Portuguesa
        tasks.append(Task(
            description=dedent(f"""
                [NOVA ANÁLISE - LÍNGUA PORTUGUESA]
                Esta é uma análise INDEPENDENTE. Ignore análises anteriores.

                TEXTO:
                {texto}

                Concentre-se APENAS em:
                1. Desvios ortográficos e acentuação
                2. Concordância verbal e nominal
                3. Regência verbal e nominal
                4. Pontuação
                5. Precisão vocabular

                NÃO analise:
                - Desenvolvimento do tema
                - Argumentação
                - Coesão
                - Proposta de intervenção

                Critérios para nota:
                200 pontos - ATRIBUA quando o texto demonstra domínio da norma culta, mesmo com um ou dois desvios pequenos. Desvios mínimos de pontuação ou uma concordância não comprometem esta nota!

                160 pontos - ATRIBUA quando há alguns desvios pontuais, mas que não comprometem a compreensão. NÃO use esta nota apenas por encontrar pequenos erros!

                120 pontos - Reserve para textos com desvios frequentes que, embora não comprometam totalmente a compreensão, demonstram domínio mediano da norma culta

                80 pontos - Use quando os desvios são frequentes e comprometem parcialmente a compreensão

                40 pontos - Reserve para casos com desvios graves e frequentes que comprometem significativamente a compreensão

                0 pontos - Use apenas quando os desvios impedem totalmente a compreensão do texto

                IMPORTANTE: Um texto bem escrito pode ter pequenos deslizes. A comunicação efetiva é mais importante que a perfeição gramatical absoluta. Se o texto comunica bem sua mensagem, pequenos desvios não devem impedir a nota máxima.

                ORIENTAÇÕES:
                - Valorize os acertos antes dos erros
                - Pequenos desvios não justificam grande perda de pontos
                - Um texto pode ser excelente mesmo não sendo perfeito
                - Reserve notas abaixo de 120 apenas para problemas graves

                Exemplo de análise:
                {{
                    "nota": [avaliar conforme critérios],
                    "justificativa": "O texto demonstra [nível] domínio da norma culta, com [pontos positivos]. [Aspectos a melhorar, se houver]",
                    "problemas": ["Desvio específico em X", "Desvio específico em Y"],
                    "sugestoes": ["Sugestão específica para X", "Sugestão específica para Y"]
                }}
            """),
            expected_output=expected_output,
            agent=agents[0]
        ))
        
        # Competência 2 - Tema
        tasks.append(Task(
            description=dedent(f"""
                [NOVA ANÁLISE - TEMA E ESTRUTURA]
                Esta é uma análise INDEPENDENTE. Ignore análises anteriores.

                TEXTO:
                {texto}

                TEMA:
                {tema}

                Concentre-se APENAS em:
                - FIDELIDADE AO TEMA: O texto aborda exatamente o tema proposto?
                - RECORTE TEMÁTICO: Como o autor delimitou o tema?
                - COMPLETUDE: Todos os aspectos importantes do tema foram contemplados?
                - ESTRUTURA TEXTUAL: Introdução, desenvolvimento e conclusão estão equilibrados?
                - INFORMATIVIDADE: As informações apresentadas são relevantes para o tema?

                ESSENCIAL: Sua função é verificar SE e COMO o tema foi desenvolvido, não a forma como o autor argumenta sobre ele.

                NÃO analise:
                - Aspectos gramaticais
                - Argumentação
                - Coesão
                - Proposta de intervenção

                Critérios para nota:
                200 pontos - ATRIBUA quando o texto aborda o tema com clareza e consistência, mesmo que algum aspecto pudesse ser mais desenvolvido. Um texto que apresenta discussão relevante e pertinente merece nota máxima!

                160 pontos - ATRIBUA quando o tema é bem desenvolvido, mesmo que falte aprofundamento em alguns pontos. NÃO use esta nota apenas por haver aspectos não contemplados!

                120 pontos - Reserve para textos que abordam o tema de forma básica, sem aprofundamento significativo, mas ainda mantendo a pertinência temática

                80 pontos - Use quando o texto tangencia o tema, abordando-o de forma superficial ou com desvios significativos

                40 pontos - Reserve para textos que apenas tocam no tema, sem desenvolvimento adequado

                0 pontos - Use apenas quando o texto foge completamente ao tema proposto

                IMPORTANTE: Valorize a pertinência e a relevância do que foi apresentado. Um texto pode desenvolver muito bem o tema mesmo sem explorar todos os aspectos possíveis. O importante é a qualidade do recorte escolhido pelo autor.

                ORIENTAÇÕES:
                - Valorize os acertos antes dos erros
                - Pequenas limitações não justificam grande perda de pontos
                - Um texto pode ser excelente mesmo não sendo perfeito
                - Reserve notas abaixo de 120 apenas para problemas graves

                Exemplo de análise:
                {{
                    "nota": [avaliar conforme critérios],
                    "justificativa": "O texto desenvolve [nível] o tema, com [pontos positivos]. [Aspectos a melhorar, se houver]",
                    "problemas": ["Aspecto específico X", "Aspecto específico Y"],
                    "sugestoes": ["Sugestão específica para X", "Sugestão específica para Y"]
                }}
            """),
            expected_output=expected_output,
            agent=agents[1]
        ))

        # Competência 3 - Argumentação
        tasks.append(Task(
            description=dedent(f"""
                [NOVA ANÁLISE - ARGUMENTAÇÃO]
                Esta é uma análise INDEPENDENTE. Ignore análises anteriores.

                TEXTO:
                {texto}

                Concentre-se APENAS em:
                - ENCADEAMENTO LÓGICO: Como os argumentos se conectam?
                - BASE ARGUMENTATIVA: Quais evidências sustentam cada argumento?
                - ESTRATÉGIAS: Uso de dados, exemplos, citações ou comparações
                - FORÇA PERSUASIVA: Os argumentos são convincentes?
                - CONCLUSÃO LÓGICA: A conclusão decorre naturalmente dos argumentos?

                ESSENCIAL: Sua função é avaliar COMO o autor defende seu ponto de vista, 
                não o tema em si ou sua abrangência.

                NÃO analise:
                - Aspectos gramaticais
                - Desenvolvimento do tema
                - Coesão
                - Proposta de intervenção

                Critérios para nota:
                200 pontos - ATRIBUA quando os argumentos são consistentes e bem fundamentados, mesmo que algum ponto pudesse ser reforçado. Argumentos pertinentes e bem articulados merecem nota máxima!

                160 pontos - ATRIBUA quando a argumentação é sólida, mesmo que algum argumento pudesse ser mais forte. NÃO use esta nota só porque um argumento poderia ser melhor!

                120 pontos - Reserve para textos com argumentação presente mas com algumas falhas na sustentação ou no desenvolvimento

                80 pontos - Use quando a argumentação é frágil, com problemas significativos de fundamentação

                40 pontos - Reserve para textos com argumentação muito precária, quase sem sustentação

                0 pontos - Use apenas quando não há argumentação desenvolvida

                IMPORTANTE: Valorize a qualidade dos argumentos apresentados. Um texto pode ter excelente argumentação mesmo sem utilizar todos os argumentos possíveis. O importante é a força e a pertinência dos argumentos utilizados.

                ORIENTAÇÕES:
                - Valorize os acertos antes dos erros
                - Pequenas falhas não justificam grande perda de pontos
                - Um texto pode ser excelente mesmo não sendo perfeito
                - Reserve notas abaixo de 120 apenas para problemas graves

                Exemplo de análise:
                {{
                    "nota": [avaliar conforme critérios],
                    "justificativa": "A argumentação apresenta [nível] desenvolvimento, com [pontos positivos]. [Aspectos a melhorar, se houver]",
                    "problemas": ["Aspecto específico X", "Aspecto específico Y"],
                    "sugestoes": ["Sugestão específica para X", "Sugestão específica para Y"]
                }}
            """),
            expected_output=expected_output,
            agent=agents[2]
        ))

        # Competência 4 - Coesão
        tasks.append(Task(
            description=dedent(f"""
                [NOVA ANÁLISE - COESÃO TEXTUAL]
                Esta é uma análise INDEPENDENTE. Ignore análises anteriores.

                TEXTO:
                {texto}

                Concentre-se APENAS em:
                1. Conectivos e elementos de ligação
                2. Referenciação (anáforas, catáforas)
                3. Progressão entre parágrafos
                4. Articulação entre ideias
                5. Recursos coesivos em geral

                NÃO analise:
                - Aspectos gramaticais
                - Desenvolvimento do tema
                - Argumentação
                - Proposta de intervenção

                Critérios para nota:
                200 pontos - ATRIBUA quando o texto apresenta boa articulação entre as ideias, mesmo com pequenos ajustes possíveis. Uma progressão clara e bem articulada merece nota máxima!

                160 pontos - ATRIBUA quando o texto é bem articulado, mesmo que algumas conexões pudessem ser mais precisas. NÃO use esta nota só por haver pequenas melhorias possíveis!

                120 pontos - Reserve para textos com articulação presente mas com algumas falhas na conexão entre ideias

                80 pontos - Use quando há problemas frequentes de articulação que prejudicam a leitura

                40 pontos - Reserve para textos com articulação muito precária entre as partes

                0 pontos - Use apenas quando não há articulação entre as ideias

                IMPORTANTE: Um texto pode ter excelente coesão mesmo sem usar todos os recursos coesivos possíveis. Valorize a eficiência das conexões estabelecidas e a clareza da progressão textual.

                ORIENTAÇÕES:
                - Valorize os acertos antes dos erros
                - Pequenas falhas não justificam grande perda de pontos
                - Um texto pode ser excelente mesmo não sendo perfeito
                - Reserve notas abaixo de 120 apenas para problemas graves

                Exemplo de análise:
                {{
                    "nota": [avaliar conforme critérios],
                    "justificativa": "O texto apresenta [nível] de coesão, com [pontos positivos]. [Aspectos a melhorar, se houver]",
                    "problemas": ["Aspecto específico X", "Aspecto específico Y"],
                    "sugestoes": ["Sugestão específica para X", "Sugestão específica para Y"]
                }}
            """),
            expected_output=expected_output,
            agent=agents[3]
        ))

        # Competência 5 - Proposta de Intervenção
        tasks.append(Task(
            description=dedent(f"""
                [NOVA ANÁLISE - PROPOSTA DE INTERVENÇÃO]
                Esta é uma análise INDEPENDENTE. Ignore análises anteriores.

                TEXTO:
                {texto}

                Concentre-se APENAS em:
                1. Detalhamento da proposta
                2. Viabilidade das ações
                3. Identificação dos agentes
                4. Meios de execução
                5. Respeito aos direitos humanos

                NÃO analise:
                - Aspectos gramaticais
                - Desenvolvimento do tema
                - Argumentação
                - Coesão textual

                Critérios para nota:
                200 pontos - ATRIBUA quando a proposta é clara, viável e bem articulada com o problema, mesmo que algum elemento pudesse ser mais detalhado. Uma proposta bem estruturada merece nota máxima!

                160 pontos - ATRIBUA quando a proposta é consistente, mesmo que falte algum detalhamento. NÃO use esta nota só porque algum aspecto poderia ser mais desenvolvido!

                120 pontos - Reserve para propostas presentes e viáveis, mas com detalhamento insuficiente

                80 pontos - Use quando a proposta é pouco desenvolvida ou tem problemas de viabilidade

                40 pontos - Reserve para propostas muito vagas ou pouco relacionadas ao problema

                0 pontos - Use apenas quando não há proposta de intervenção

                IMPORTANTE: Uma proposta pode ser excelente mesmo sem esgotar todas as possibilidades. Valorize a pertinência, a viabilidade e o respeito aos direitos humanos na solução apresentada.

                ORIENTAÇÕES:
                - Valorize os acertos antes dos erros
                - Pequenas falhas não justificam grande perda de pontos
                - Uma proposta pode ser excelente mesmo não sendo perfeita
                - Reserve notas abaixo de 120 apenas para problemas graves

                Exemplo de análise:
                {{
                    "nota": [avaliar conforme critérios],
                    "justificativa": "A proposta apresenta [nível] desenvolvimento, com [pontos positivos]. [Aspectos a melhorar, se houver]",
                    "problemas": ["Aspecto específico X", "Aspecto específico Y"],
                    "sugestoes": ["Sugestão específica para X", "Sugestão específica para Y"]
                }}
            """),
            expected_output=expected_output,
            agent=agents[4]
        ))

        return tasks