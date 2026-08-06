# StudyBot - Bot de Estudos para Bug Bounty (Discord)

Bot profissional para organização de estudos de segurança ofensiva.
Cria automaticamente toda a estrutura do servidor e gerencia progresso, notas e templates.

## Instalação

1. Clone o repositório (ou execute `setup_projeto.py` para gerar tudo).
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Crie um arquivo `.env` baseado no `.env.example` e adicione seu token:
   ```
   DISCORD_TOKEN=seu_token_aqui
   ```
4. Execute o bot:
   ```bash
   python bot.py
   ```

## Como criar o bot no Discord

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications).
2. Crie uma nova aplicação e vá até a seção 'Bot'.
3. Clique em 'Add Bot' e copie o token.
4. Ative os **Privileged Gateway Intents** (Presence, Server Members, Message Content).

## Como adicionar ao servidor

1. No portal, vá em 'OAuth2' > 'URL Generator'.
2. Marque os escopos: `bot`, `applications.commands`.
3. Permissões necessárias: `Administrator` (ou manualmente: Manage Channels, Manage Messages, etc.).
4. Acesse a URL gerada e selecione seu servidor.

## Comandos

| Comando      | Descrição                                          |
|--------------|----------------------------------------------------|
| `/setup`     | Cria categorias e canais automaticamente.          |
| `/progresso` | Mostra seu progresso no roadmap.                   |
| `/proximo`   | Sugere o próximo tópico a estudar.                 |
| `/concluir`  | Marca o tópico atual como concluído.               |
| `/reabrir`   | Remove a conclusão do tópico atual.                |
| `/roadmap`   | Lista todos os tópicos do roadmap com status.      |
| `/topico`    | Cria um novo canal com template personalizado.     |
| `/hipotese`  | Cria uma thread para hipóteses.                    |
| `/lab`       | Cria uma thread para laboratório prático.          |
| `/writeup`   | Cria uma thread para writeup de vulnerabilidade.   |
| `/nota`      | Salva uma nota no banco de dados.                  |
| `/search`    | Pesquisa em notas e templates.                     |
| `/stats`     | Estatísticas do servidor (admin).                  |
| `/help`      | Exibe todos os comandos.                           |

## Personalização

### Templates
Edite o arquivo `data/templates.json`.  
Cada chave corresponde ao nome de um canal ou a um identificador usado pelo `/topico`.

### Roadmap
Edite `data/roadmap.json` para alterar a ordem dos tópicos ou adicionar novos.

### Categorias e canais
Edite `data/categories.json` para modificar a estrutura criada pelo `/setup`.

## Configurações adicionais
- `data/config.json` contém o template padrão e limites de pesquisa.
- O banco de dados SQLite é gerado automaticamente em `database/study.db`.

## Logs
Todos os eventos importantes são registrados no console. Para produção, redirecione para um arquivo.

## Licença
MIT
