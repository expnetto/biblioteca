# Sistema de Gerenciamento de Biblioteca

Atividade prática da disciplina de Linguagens de Programação, integrando
Programação Orientada a Objetos e Programação Funcional.

**Aluno:** Eraldo Xavier Pimentel Netto
**Modalidade:** individual
**Linguagem:** Python 3.10+ (desenvolvido e testado em Python 3.14.7)
**Dependências de execução:** nenhuma, apenas a biblioteca padrão

## Como executar

```
python3 main.py
```

O programa abre pedindo a escolha de um cenário pré-carregado e segue em um menu
interativo. Nenhum dado é gravado em disco: tudo vive em memória durante a
execução.

## Como rodar os testes

```
pip3 install -r requirements-dev.txt
python3 -m pytest
```

`pytest` é dependência apenas de teste. O sistema roda sem ela.

## Funcionalidades

- Cadastro de livros e de usuários, com recusa de identificador ou matrícula repetidos
- Consulta de livros: todos, somente disponíveis ou filtrados por categoria
- Consulta de usuários
- Registro de empréstimos, com verificação de disponibilidade do livro
- Registro de devoluções, que libera o livro para novos empréstimos
- Consulta de empréstimos: todos, somente ativos ou ativos em atraso numa data
- Relatório de multas por data de referência
- Estatísticas do acervo e da circulação
- Comparação entre a versão imperativa e a funcional do cálculo do total de multas
- Quatro cenários pré-carregados, trocáveis sem sair do programa

## Regras de negócio implementadas

1. Um usuário pode ter vários empréstimos; cada empréstimo é de um único livro e de um único usuário.
2. Um livro não pode estar emprestado para mais de um usuário ao mesmo tempo.
3. Cada livro cadastrado é um exemplar único, sem controle de múltiplas cópias.
4. A devolução registra a data e torna o livro disponível novamente.
5. Um empréstimo está atrasado quando a data prevista de devolução foi ultrapassada e o livro ainda não foi devolvido. O dia exato do vencimento não é atraso.
6. A multa é de R$ 2,00 por dia de atraso. Empréstimos sem atraso não geram multa.
7. O relatório de multas considera apenas os empréstimos ativos e atrasados, a partir de uma data de referência informada.
8. Não há reservas, múltiplos exemplares nem multa para empréstimos já devolvidos — inclusive os devolvidos com atraso.

## Arquitetura

A fronteira entre o que é puro e o que tem efeito colateral está na estrutura de
arquivos, não apenas na intenção:

| Arquivo | Natureza | Responsabilidade |
|---|---|---|
| `biblioteca/dominio.py` | imutável | `Livro`, `Usuario` e `Emprestimo` como dataclasses congeladas |
| `biblioteca/biblioteca.py` | **impuro** | `Biblioteca`: único estado mutável do sistema |
| `biblioteca/consultas.py` | puro | filtragens de livros e empréstimos, disponibilidade, geração de identificador |
| `biblioteca/multas.py` | puro | cálculo de multa e relatório com `filter`, `map` e `reduce` |
| `biblioteca/estatisticas.py` | puro | as cinco estatísticas |
| `biblioteca/comparacao.py` | puro | as duas versões do total de multas, imperativa e funcional |
| `biblioteca/cenarios.py` | **impuro** | fábricas que constroem bibliotecas povoadas |
| `biblioteca/cli.py` | **impuro** | único ponto do projeto com `input()` e `print()` |

### Fluxo do relatório de multas

```
cli.py                        impuro   lê a data de referência digitada
Biblioteca.relatorio_de_multas  impuro   lê o estado interno e devolve cópia imutável
emprestimos_atrasados          puro     filter  seleciona ativos e vencidos
multa_do_emprestimo via map    puro     map     calcula a multa de cada um
soma via reduce                puro     reduce  agrega em um total
RelatorioMultas                puro     resultado imutável
cli.py                         impuro   imprime
```

### Decisões de projeto

**Imutabilidade.** `Livro`, `Usuario` e `Emprestimo` são `@dataclass(frozen=True)`:
qualquer tentativa de alterar um atributo levanta `FrozenInstanceError`. A
devolução não altera o empréstimo — `Emprestimo.devolvido_em()` devolve uma
instância nova. Todas as funções puras devolvem `tuple`, nunca `list`, para que o
resultado não possa ser alterado por engano. As estatísticas de contagem usam
`reduce` criando um dicionário novo a cada passo, sem nunca mutar o acumulador.

**Encapsulamento.** A `Biblioteca` é a única classe com estado mutável. Suas
coleções (`_livros`, `_usuarios`, `_emprestimos`) são privadas e nunca devolvidas
diretamente: os métodos de consulta devolvem tuplas. Nas entidades, o
encapsulamento é obtido por congelamento em vez de getters e setters — `frozen=True`
é proteção mais forte que um setter, porque não há como alterar o estado nem de
fora nem de dentro. As entidades também não são sacos de dados: `Emprestimo`
carrega o próprio comportamento (`esta_ativo`, `esta_atrasado`, `dias_de_atraso`,
`devolvido_em`).

**Disponibilidade é derivada, não armazenada.** Não existe campo booleano
`disponivel` no `Livro`. Um livro está disponível quando não há empréstimo ativo
com ele, o que é verificado pela função pura `esta_disponivel`. Guardar a
disponibilidade em dois lugares — no livro e na lista de empréstimos — abriria
espaço para os dois discordarem.

**Erros não são silenciosos.** As operações da `Biblioteca` levantam exceções
próprias (`IdentificadorDuplicadoError`, `CadastroInexistenteError`,
`LivroIndisponivelError`, `EmprestimoInexistenteError`, `EmprestimoJaDevolvidoError`)
em vez de devolver `None` ou imprimir. Quem decide como mostrar o erro é o CLI.

**Separação de paradigmas.** Nenhuma função pura recebe a `Biblioteca`: todas
recebem coleções e devolvem dados novos. Por isso o cálculo de multas e as
estatísticas são testáveis sem instanciar nada. Os métodos
`Biblioteca.relatorio_de_multas` e `Biblioteca.estatisticas` são adaptadores de
três linhas que apenas repassam os próprios dados às funções puras.

## Comparação entre paradigmas

`biblioteca/comparacao.py` implementa o total das multas de duas maneiras:

- `total_de_multas_funcional` — `filter` seleciona os atrasados, `map` converte cada um em valor e `reduce` soma. Não há variável reatribuída e nenhum dado é alterado.
- `total_de_multas_imperativo` — um laço `for`, dois `if` encadeados e um acumulador `total` reatribuído a cada volta.

O teste `test_as_duas_versoes_concordam_em_todos_os_cenarios` verifica a
equivalência nos três cenários povoados e em quatro datas de referência
diferentes, além dos casos de borda: coleção vazia, ninguém atrasado, todos
atrasados e devolvido com atraso.

O que se observa na comparação: a versão funcional descreve **o que** é calculado
em três etapas nomeadas, enquanto a imperativa descreve **como**, misturando a
seleção, o cálculo e a agregação dentro do mesmo laço. A funcional não tem estado
intermediário — não existe um `total` parcialmente correto em nenhum momento — e
cada etapa é testável isoladamente. A imperativa repete por dentro a regra de
atraso que a versão funcional obtém de `esta_atrasado`, o que é exatamente o tipo
de duplicação que faz as duas se separarem quando a regra mudar.

## Onde cada requisito do enunciado foi atendido

| Requisito | Onde |
|---|---|
| Quatro classes e relacionamentos (§3) | `dominio.py`, `biblioteca.py` |
| Responsabilidades da `Biblioteca` (§3.4) | `biblioteca.py` |
| Regras de negócio 1 a 8 (§4) | `biblioteca.py`, `dominio.py`, `multas.py` |
| Filtragem de livros por categoria (§5.1) | `consultas.filtrar_livros_por_categoria` |
| Cálculo de multa como função pura (§5.2) | `multas.calcular_multa` |
| Empréstimos atrasados (§5.3) | `multas.emprestimos_atrasados` |
| Relatório com `filter`, `map` e `reduce` (§5.4) | `multas.relatorio_de_multas` |
| As cinco estatísticas (§5.5) | `estatisticas.py` |
| Imutabilidade (§5.6) | `frozen=True`, retornos em `tuple`, `reduce` sem mutação |
| Comparação de paradigmas (§6) | `comparacao.py` |
| Mínimo de três funções puras (§7) | doze funções puras em `consultas.py`, `multas.py` e `estatisticas.py` |
| `reduce` no relatório e em estatística (§7) | `multas.relatorio_de_multas`, `estatisticas.quantidade_de_livros_por_categoria`, `estatisticas.quantidade_de_emprestimos_por_usuario` |
| Separação puro/impuro (§7) | tabela de arquitetura acima |
| Executar e demonstrar (§7) | `main.py` e `cli.py`, com quatro cenários |
| Nomes claros (§7) | todo o código |
| Sem comentários (§7) | nenhum comentário ou docstring em nenhum arquivo |

## Testes

68 testes, organizados por módulo:

| Arquivo | Cobre |
|---|---|
| `tests/test_dominio.py` | congelamento das entidades, atraso no dia exato do vencimento, devolução sem alterar o original |
| `tests/test_consultas.py` | filtragem por categoria, disponibilidade antes e depois da devolução, geração de identificador |
| `tests/test_multas.py` | multa com zero, um, vários e dias negativos, transparência referencial, relatório que ignora devolvidos |
| `tests/test_estatisticas.py` | as cinco estatísticas, acervo vazio, usuários homônimos |
| `tests/test_comparacao.py` | equivalência entre as duas versões em todos os cenários e casos de borda |
| `tests/test_biblioteca.py` | duplicatas recusadas, livro não emprestado duas vezes, devolução repetida recusada |
