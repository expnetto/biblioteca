# Sistema de Gerenciamento de Biblioteca — Design

Disciplina: Linguagens de Programação (Orientação a Objetos e Programação Funcional)
Aluno: Eraldo Xavier Pimentel Netto
Modalidade escolhida: individual
Linguagem: Python
Data do design: 2026-10-28
Entrega: 02/12/2026

## 1. Intenção e o porquê

Entregar um sistema de gerenciamento de biblioteca em memória que integre POO e
programação funcional, conforme o enunciado da atividade prática, e que seja
**defensável oralmente em qualquer ponto** por quem o escreveu.

O aluno fará a atividade individualmente e **abriu mão, por decisão própria, dos
2,0 pontos da apresentação individual**. A meta é a faixa de 3,0 pontos da
entrega do projeto e dos manuscritos; ele precisa de 1,0 ponto para ser
aprovado. Ele estará presente para entregar os manuscritos fisicamente ao
professor.

Isso desloca o centro de gravidade do projeto. Como não haverá apresentação, o
que o professor vai avaliar são três artefatos de papel e código: o repositório,
o README e os dois diagramas manuscritos. O enunciado exige que o Diagrama de
Fluxo de Processamento Funcional case **bloco a bloco** com o código real, com
cada etapa classificada como pura ou impura, e avisa que diagramas genéricos ou
incompatíveis com o código não serão aceitos. Portanto o código precisa ter uma
espinha dorsal funcional nítida e curta o bastante para ser desenhada à mão sem
consulta. Essa é a restrição de projeto mais importante deste documento, e ela
vale mais que elegância, generalidade ou cobertura de casos.

O segundo motor é autoria. O aluno quer um projeto autoral, e as cinco questões
manuscritas pedem que ele aponte uma função pura sua, uma operação impura sua, e
compare suas próprias versões imperativa e funcional. Código que ele não consiga
explicar não serve, mesmo que funcione.

## 2. Metas, não-metas e anti-metas

### Metas
- Cumprir integralmente os requisitos técnicos obrigatórios da Seção 7 do enunciado.
- Um pipeline de relatório de multas com `filter` → `map` → `reduce` explícito e desenhável de memória.
- Fronteira pura/impura visível na estrutura de arquivos, não apenas na intenção.
- CLI interativo capaz de demonstrar mais de um cenário ao vivo.
- README que sirva de documentação completa, já que o código não pode ter comentários.
- Testes que provem que multa, atraso e disponibilidade estão corretos.
- Código que o aluno consiga explicar linha a linha.

### Não-metas
- **Apresentação individual (2,0 pontos) — abandonada por decisão do aluno.** Registre-se com clareza: a Seção 11 do enunciado lista a "participação individual na apresentação e resposta à pergunta sobre o projeto" como entrega individual **obrigatória**. É o único requisito do enunciado que este projeto deliberadamente não cumprirá, e a decisão é do aluno, informado de que isso custa 2,0 dos 5,0 pontos. Nenhuma escolha técnica deste documento o substitui, e nenhum ajuste de código o compensa.
- Banco de dados ou qualquer persistência. Tudo em memória.
- Reservas, múltiplos exemplares do mesmo livro, multa para empréstimos já devolvidos.
- Interface web, GUI, API HTTP.
- Bibliotecas externas de runtime. Apenas biblioteca padrão (`pytest` é permitido como dependência só de teste).
- Concorrência real, threads, locks. A questão E é conceitual e se responde no papel.

### Anti-metas (reprovariam o trabalho mesmo funcionando)
- `map`/`filter`/`reduce` usados decorativamente sobre código que na verdade muta estado. O enunciado alerta explicitamente contra isso.
- Qualquer comentário no código-fonte: de linha, de bloco ou explicação embutida. É proibição expressa e fácil de verificar.
- Mutabilidade escondida: expor listas internas da `Biblioteca` para que funções "puras" as alterem.
- Um diagrama que não corresponda ao código entregue.
- Código grande ou abstrato demais para o aluno desenhar e defender.

## 3. Restrições

- Python 3.14.7, que é o que está instalado na máquina do aluno (`python3`). Nada no projeto exige versão recente; declare 3.10+ como mínimo no README por causa da sintaxe `X | None`.
- Somente biblioteca padrão em runtime: `dataclasses`, `datetime`, `functools.reduce`, `typing`.
- `pytest` não está instalado. O builder instala (`pip3 install pytest`) e registra em `requirements-dev.txt`, deixando claro no README que é dependência só de teste e que o sistema roda sem ela.
- Proibido qualquer comentário no código-fonte, em todos os arquivos, inclusive nos testes.
- Dados em memória; nenhuma gravação em disco.
- Manuscritos: inteiramente à mão, em papel A4 branco sem pautas nem quadriculados, **cada folha identificada com o nome completo** (Eraldo Xavier Pimentel Netto), legíveis e entregues fisicamente ao professor. Produzido digitalmente e impresso não é aceito, nem para os diagramas nem para as respostas.
- Multa fixada em R$ 2,00 por dia de atraso no relatório; a função de cálculo, porém, recebe o valor diário como parâmetro (exigência da Seção 5.2).
- O relatório de multas considera **apenas empréstimos ativos e atrasados**, com data de referência recebida como parâmetro.
- Cada livro é exemplar único.

## 4. Decisões já tomadas

### Tomadas pelo aluno
- Modalidade individual.
- Linguagem Python.
- Abrir mão dos 2,0 pontos da apresentação; mirar os 3,0 pontos restantes.
- Estar presente para a entrega física dos manuscritos.
- **CLI interativo**, com menu, em vez de um script de cenário fixo — ele quer poder mostrar mais de um cenário ao vivo e navegar.
- Grilling sobre o próprio código ao final, como preparação para os manuscritos (ver Seção 10).

### Tomadas pelo Claude (não ratificadas pelo aluno; revisáveis)
- Entidades como `@dataclass(frozen=True)`, para que a imutabilidade seja garantida pela linguagem e não por convenção. Dá uma resposta concreta e verificável à questão C. **Risco conhecido:** um corretor que espere encapsulamento no formato clássico (atributos privados com getters e setters) pode estranhar atributos públicos nas entidades. O argumento, que deve constar do README, é que `frozen=True` é uma proteção mais forte que um setter — não há como alterar o estado de fora, nem de dentro — e que as entidades não são sacos de dados: `Emprestimo` carrega comportamento próprio (`esta_ativo`, `esta_atrasado`, `dias_de_atraso`, `devolvido_em`). O encapsulamento no sentido clássico, com coleções privadas e acesso controlado, está na `Biblioteca`, que é a classe que de fato guarda estado mutável.
- `datetime.date` para datas; `timedelta.days` para a diferença.
- `Emprestimo` guarda os **objetos** `Livro` e `Usuario`, não os identificadores. O enunciado pede relacionamentos entre objetos e multiplicidades no UML, e objetos aninhados tornam o diagrama de classes honesto. Como são frozen, não há risco de aliasing mutável.
- Testes incluídos, com `pytest`, apesar de não constarem da lista de entrega do PDF. Eles são a prova de que a multa e os atrasos estão certos e o seguro contra um erro silencioso de data.
- Nenhuma docstring. O enunciado proíbe "explicações embutidas", e docstring é explicação embutida. Anotações de tipo ficam, porque são declaração, não comentário.
- A comparação imperativa × funcional da Seção 6 recai sobre o **relatório de multas**, que é a função mais rica para contrastar legibilidade, mutabilidade e acumuladores.
- Repositório GitHub **público**, para que o professor acesse pelo link sem precisar de convite. Criado via `gh` CLI (instalado nesta sessão, versão 2.103.3), a pedido do aluno; falta apenas `gh auth login`, que é interativo.
- Coleções devolvidas como `tuple`, não `list`, nas funções puras e nos acessores da `Biblioteca`: torna impossível alterar por acidente o que foi devolvido.
- As estatísticas de contagem devolvem `dict` comum, não `tuple` de pares nem `MappingProxyType`. É a estrutura que o professor espera ver para "quantidade por categoria", e a pureza aqui vem de outro lugar: o dicionário é construído novo a cada chamada e o `reduce` **nunca muta o acumulador**, criando um dicionário novo por passo (`{**acumulado, chave: acumulado.get(chave, 0) + 1}`). É O(n²), e isso é aceito de propósito: o volume é de demonstração e o custo paga a demonstração explícita de imutabilidade, que é justamente o que está sendo avaliado. O builder deve saber disso para responder se for perguntado.

## 5. Modelagem orientada a objetos

Quatro classes, como o enunciado determina.

### Imutáveis (`biblioteca/dominio.py`)

`Livro` — frozen dataclass: `identificador: str`, `titulo: str`, `autor: str`, `categoria: str`.

`Usuario` — frozen dataclass: `identificador: str`, `nome: str`, `matricula: str`.

`Emprestimo` — frozen dataclass: `identificador: str`, `livro: Livro`, `usuario: Usuario`,
`data_emprestimo: date`, `data_prevista_devolucao: date`, `data_devolucao: date | None`.

`Emprestimo` expõe consultas sem efeito colateral, que são métodos puros sobre o próprio objeto:
- `esta_ativo() -> bool` — verdadeiro quando `data_devolucao is None`.
- `esta_atrasado(data_referencia: date) -> bool` — ativo **e** `data_prevista_devolucao < data_referencia`.
- `dias_de_atraso(data_referencia: date) -> int` — zero quando não atrasado; caso contrário a diferença em dias.

A devolução **não** altera o empréstimo: produz um novo. Isso é o coração da
resposta à questão C.
- `devolvido_em(data: date) -> Emprestimo` — devolve uma nova instância com `data_devolucao` preenchida (`dataclasses.replace`).

### Mutável (`biblioteca/biblioteca.py`)

`Biblioteca` é a única classe com estado mutável e a única fronteira impura do
domínio. Mantém `_livros`, `_usuarios` e `_emprestimos` privados e nunca os
devolve diretamente.

Operações de gerenciamento (impuras, alteram estado):
- `cadastrar_livro(livro)`, `cadastrar_usuario(usuario)` — recusam identificador já cadastrado. A regra 3 do enunciado trata cada livro como exemplar único, e a disponibilidade é derivada do identificador: dois livros com o mesmo identificador quebrariam silenciosamente o controle de disponibilidade e a contagem por categoria. A matrícula do usuário também é recusada se repetida.
- `registrar_emprestimo(livro, usuario, data_emprestimo, data_prevista_devolucao) -> Emprestimo` — recusa se o livro não estiver disponível (regra 2) ou se livro/usuário não estiverem cadastrados. Gera o identificador do empréstimo.
- `registrar_devolucao(identificador_emprestimo, data_devolucao) -> Emprestimo` — substitui o empréstimo ativo pela nova instância devolvida; o livro volta a ficar disponível (regra 4). Recusa se já devolvido ou inexistente.

Consultas (devolvem cópias imutáveis; não alteram nada):
- `livros() -> tuple[Livro, ...]`, `usuarios() -> tuple[Usuario, ...]`, `emprestimos() -> tuple[Emprestimo, ...]`
- `buscar_livro(identificador)`, `buscar_usuario(identificador)`

Adaptadores de relatório e estatística (impuros apenas porque leem o estado
interno; não calculam nada por conta própria):
- `relatorio_de_multas(data_referencia) -> RelatorioMultas`
- `estatisticas(data_referencia) -> Estatisticas`

A Seção 3.4 do enunciado atribui à `Biblioteca` a responsabilidade de
"disponibilizar os dados de relatórios e estatísticas". Estes dois métodos são
adaptadores de três linhas: pegam `self.emprestimos()` e `self.livros()` e
repassam às funções puras dos módulos funcionais, devolvendo o resultado sem
tocá-lo. Nenhuma regra de cálculo vive aqui — se alguma lógica de multa ou
contagem aparecer dentro da classe, o builder errou. A separação exigida pela
Seção 5.6 continua intacta: o cálculo é puro e testável sem instanciar a
`Biblioteca`, e a classe apenas cumpre a responsabilidade que o enunciado lhe
deu.

Recusas usam exceções próprias (`LivroIndisponivelError`, `EmprestimoInexistenteError`,
`EmprestimoJaDevolvidoError`, `CadastroInexistenteError`,
`IdentificadorDuplicadoError`), não `None` nem `print`:
a `Biblioteca` sinaliza o erro, e é o CLI que decide como mostrá-lo. Sem falha
silenciosa.

Disponibilidade **não** é um campo booleano no `Livro`. É derivada: um livro está
disponível quando não existe empréstimo ativo com ele. Isso evita dois lugares
guardando a mesma verdade e permite que a checagem seja uma função pura. O
builder deve registrar essa decisão no README, porque é uma pergunta natural do
professor.

## 6. Camada funcional

Tudo aqui é função pura de módulo: recebe dados, devolve dados novos, não
imprime, não altera entrada, não lê relógio. Nenhuma delas recebe a
`Biblioteca`; recebem coleções. É assim que a fronteira fica visível.

### `biblioteca/consultas.py`
- `filtrar_livros_por_categoria(livros, categoria) -> tuple[Livro, ...]` — Seção 5.1, com `filter`.
- `esta_disponivel(livro, emprestimos) -> bool`
- `livros_disponiveis(livros, emprestimos) -> tuple[Livro, ...]` — com `filter`.
- `emprestimos_ativos(emprestimos) -> tuple[Emprestimo, ...]` — com `filter`.

### `biblioteca/multas.py` — a espinha dorsal
- `calcular_multa(dias_atraso: int, valor_diario: float) -> float` — Seção 5.2. Pura, total, sem recorrer a nada externo: dias não positivos devolvem `0.0`. É a função a citar na questão A.
- `emprestimos_atrasados(emprestimos, data_referencia) -> tuple[Emprestimo, ...]` — Seção 5.3, com `filter`.
- `multa_do_emprestimo(emprestimo, data_referencia, valor_diario) -> ItemMulta` — monta o registro do relatório (frozen dataclass `ItemMulta`: empréstimo, usuário, livro, dias de atraso, valor).
- `relatorio_de_multas(emprestimos, data_referencia, valor_diario=VALOR_MULTA_DIARIA) -> RelatorioMultas` — Seção 5.4. Obrigatoriamente, e nesta ordem:
  1. `filter` → seleciona os ativos e atrasados;
  2. `map` → transforma cada um em `ItemMulta`;
  3. `reduce` → soma os valores em um total.
  Devolve `RelatorioMultas` (frozen dataclass: `itens: tuple[ItemMulta, ...]`, `total: float`, `data_referencia: date`).

`VALOR_MULTA_DIARIA = 2.00` é uma constante de módulo. O relatório a usa como
padrão; a função de cálculo nunca a lê por dentro, recebe sempre por parâmetro.

### `biblioteca/estatisticas.py` — Seção 5.5
- `quantidade_de_livros_por_categoria(livros) -> dict[str, int]` — **com `reduce`**, acumulando em dicionários novos a cada passo, nunca mutando o acumulador.
- `quantidade_de_emprestimos_por_usuario(emprestimos) -> dict[str, int]` — **com `reduce`**, mesmo padrão. A chave é o **identificador** do usuário, não o nome: nomes podem repetir e a contagem ficaria errada. O CLI resolve o identificador para o nome só na hora de imprimir.
- `quantidade_de_emprestimos_ativos(emprestimos) -> int`
- `quantidade_de_emprestimos_ativos_em_atraso(emprestimos, data_referencia) -> int`
- `valor_total_das_multas(emprestimos, data_referencia) -> float`

Isso satisfaz com folga a exigência de `reduce` em ao menos uma estatística, além
do uso obrigatório no relatório.

### `biblioteca/comparacao.py` — Seção 6
Duas implementações do mesmo relatório, lado a lado no mesmo arquivo, para o
contraste ser óbvio a olho nu:
- `total_de_multas_funcional(emprestimos, data_referencia)` — `filter` + `map` + `reduce`.
- `total_de_multas_imperativo(emprestimos, data_referencia)` — laço `for`, condicional e acumulador local.

Um teste dedicado afirma que as duas devolvem o mesmo resultado para as mesmas
entradas, inclusive nos casos de borda (lista vazia, nenhum atrasado, todos
atrasados). A versão imperativa existe para ser comparada, não para ser usada: o
CLI chama a funcional.

## 7. Interface (`biblioteca/cli.py` e `main.py`)

O CLI é a **única** camada impura fora da `Biblioteca`: é o único lugar do
projeto com `input()` e `print()`. Essa concentração é deliberada e é o que o
aluno vai apontar na questão B.

`main.py` na raiz é o ponto de entrada: `python main.py`.

Na abertura, o CLI oferece a escolha de um cenário pré-carregado
(`biblioteca/cenarios.py`). Essas funções são **fábricas impuras**, não funções
puras: cada uma instancia uma `Biblioteca` e chama os métodos de cadastro e de
empréstimo, que alteram estado. Elas não imprimem nem leem entrada, e para a
mesma chamada produzem sempre um estado equivalente, mas construir objeto mutável
é efeito colateral, e chamá-las de puras seria exatamente o tipo de confusão
contra o qual a Seção 13 do enunciado adverte. No diagrama de fluxo e na questão B
elas entram do lado impuro, ao lado do `cli` e da `Biblioteca`. Cenários:
1. **Com atrasos** — vários empréstimos, alguns vencidos há dias diferentes.
2. **Em dia** — nenhum atraso; o relatório sai vazio e o total zero.
3. **Misto** — ativos em dia, ativos atrasados e devolvidos (inclusive um
   devolvido com atraso, que **não** gera multa — regra 8, e um bom ponto para
   mostrar ao professor).
4. **Vazio** — começar sem dados e cadastrar tudo na hora.

Menu principal, em laço até sair:
- cadastrar livro; cadastrar usuário
- listar livros (todos / só disponíveis / por categoria)
- listar usuários
- registrar empréstimo; registrar devolução
- listar empréstimos (todos / ativos / atrasados em uma data)
- **relatório de multas**, pedindo a data de referência
- **estatísticas**, pedindo a data de referência
- comparação imperativa × funcional, exibindo os dois resultados e que coincidem
- trocar de cenário sem sair do programa

A data de referência é sempre digitada, nunca `date.today()` implícito dentro das
funções puras. Ela é o que transforma a demonstração: a mesma coleção de
empréstimos produz relatórios diferentes só mudando esse parâmetro, e nada nos
dados é alterado. O builder deve garantir que isso seja fácil de exibir — de
preferência, oferecer "hoje" como sugestão, mas passando o valor adiante como
argumento explícito.

Entrada inválida (data mal formatada, opção inexistente, identificador que não
existe) devolve mensagem clara e volta ao menu. Sem travar, sem stack trace na
cara do professor, sem engolir o erro em silêncio.

## 8. Estrutura de arquivos

```
biblioteca/
  main.py
  README.md
  .gitignore
  biblioteca/
    __init__.py
    dominio.py
    biblioteca.py
    consultas.py
    multas.py
    estatisticas.py
    comparacao.py
    cenarios.py
    cli.py
  tests/
    test_dominio.py
    test_biblioteca.py
    test_consultas.py
    test_multas.py
    test_estatisticas.py
    test_comparacao.py
  docs/
    superpowers/specs/2026-10-28-sistema-biblioteca-design.md
```

A separação de arquivos é o argumento visual da arquitetura: `dominio.py` e
`biblioteca.py` são POO, `consultas.py`/`multas.py`/`estatisticas.py` são puros,
`cli.py` é a borda impura. Um olhar na árvore já conta a história.

## 9. Testes

`pytest`. Sem comentários nos testes também; o nome de cada teste diz o que ele
afirma. O que precisa estar coberto:

- `calcular_multa`: zero dias, um dia, vários dias, dias negativos; mesma entrada
  → mesma saída (transparência referencial, verificável).
- `dias_de_atraso` e `esta_atrasado`: antes do vencimento, no dia exato do
  vencimento (não é atraso), depois, e empréstimo já devolvido (nunca atrasado).
- Devolvido com atraso não entra no relatório nem gera multa (regra 8).
- `registrar_emprestimo` recusa livro já emprestado (regra 2) e aceita depois da
  devolução (regra 4).
- `registrar_devolucao` produz um **novo** `Emprestimo` e não altera o original.
- Imutabilidade: as funções puras não alteram a coleção recebida — compare a
  coleção antes e depois; as entidades recusam atribuição (`FrozenInstanceError`).
- `relatorio_de_multas`: lista vazia → total zero e itens vazios; total igual à
  soma manual; não altera a entrada.
- Estatísticas: contagens por categoria e por usuário corretas, coleção vazia
  tratada.
- Equivalência imperativa × funcional.

## 10. Preparação para os manuscritos e para o grilling

Esta seção é parte do trabalho, não um apêndice: os manuscritos valem tanto
quanto o código na faixa dos 3,0 pontos, e são individuais e intransferíveis.

**Ordem obrigatória:** o código é congelado **antes** de desenhar. O Diagrama de
Fluxo precisa casar bloco a bloco com o código entregue, então qualquer renomeação
posterior invalida o desenho.

Ao final da implementação, o builder deve produzir, **no README ou em um
documento auxiliar** (nunca no código), o material de apoio aos manuscritos:

- **Diagrama de Classes (UML)**: as quatro classes com atributos e métodos
  principais, relacionamentos e multiplicidades — `Usuario 1 → * Emprestimo`,
  `Livro 1 → * Emprestimo` (único ativo por vez), `Biblioteca 1 → *` para as três
  — e a responsabilidade de cada classe em uma linha. O aluno desenha à mão a
  partir disso.
- **Diagrama de Fluxo Funcional** do relatório de multas: a cadeia de blocos com,
  em cada um, nome da função, dados recebidos, resultado produzido, classificação
  pura/impura e qual operação funcional foi usada. A cadeia é:
  `cli` (impuro, lê a data digitada) → `Biblioteca.relatorio_de_multas(data)` (impuro,
  lê o estado interno e devolve cópia) → `emprestimos_atrasados` (puro, `filter`) →
  `multa_do_emprestimo` via `map` (puro) → soma via `reduce` (puro) →
  `RelatorioMultas` → `cli` imprime (impuro).
- **Insumos das cinco questões**, com a referência exata de arquivo e função para
  cada uma: A → `calcular_multa`; B → `cli.py` ou `registrar_emprestimo`;
  C → `frozen=True`, `devolvido_em`, retorno em `tuple`; D → `comparacao.py`;
  E → a corrida entre dois empréstimos do mesmo livro, onde a resposta é **não**:
  pureza e imutabilidade eliminam a corrida *de dados*, mas não a condição de
  corrida sobre a decisão de disponibilidade, que precisa de serialização,
  transação ou lock no ponto que muta a `Biblioteca`.

Depois disso, uma sessão de grilling sobre o código implementado — perguntas no
estilo do professor, respondidas apontando o próprio código —, cobrindo também
partes que o aluno escreveu rápido. Essa sessão não produz entregável; produz
fluência.

## 11. README (entregável)

Como o código não pode ter comentários, o README é toda a documentação. Deve ter:
nome completo do aluno — Eraldo Xavier Pimentel Netto (entrega individual; o
enunciado pede os nomes de todos os integrantes), linguagem e versão, como instalar e executar (`python main.py`),
como rodar os testes, lista de funcionalidades, onde cada requisito obrigatório
do enunciado foi atendido (mapa requisito → arquivo/função), explicação das regras
de negócio implementadas, a decisão de disponibilidade derivada em vez de campo
booleano, e a comparação imperativa × funcional com o que se observa nela.

## 12. O que fica a cargo do builder

- Formato e geração dos identificadores de livro, usuário e empréstimo.
- Formatação da saída no terminal (tabelas, alinhamento, formato monetário).
- Assinaturas exatas, nomes dos arquivos de teste e organização interna de cada módulo.
- Conteúdo concreto dos quatro cenários (títulos, autores, categorias, nomes, datas).
- Prazo de devolução padrão sugerido pelo CLI ao registrar um empréstimo.
- Se a validação de data aceita um ou mais formatos de entrada.
- Como apresentar o mapa requisito → código no README.

---

## 13. Ajustes feitos depois da implementação (2026-10-29)

O código foi revisado com um critério que não estava neste documento e passou a
estar: **nada deve ficar acima do nível da disciplina**, porque o aluno precisa
conseguir explicar qualquer linha sem apoio. Um recurso elegante que ele não
saiba defender vale menos que um recurso simples que ele domine. As mudanças:

1. `from __future__ import annotations` removido de todos os arquivos. Era ruído
   desnecessário em Python 3.14 e difícil de justificar numa pergunta.
2. Anotações de tipo passaram de `Iterable[Livro]` para `tuple[Livro, ...]`.
   Tipos concretos, sem o conceito de protocolo de iteração por trás.
3. `Emprestimo.devolvido_em` constrói o novo objeto campo por campo em vez de usar
   `dataclasses.replace`. Fica mais verboso e mais explicável: dá para apontar o
   objeto novo sendo criado, que é justamente o argumento da questão C.
4. `proximo_identificador` passou a receber a quantidade já cadastrada em vez de
   derivar o maior número existente com `map`, `filter`, fatiamento de string e
   `max(..., default=0)`. A versão anterior era quatro vezes maior e resolvia um
   problema que não existe, porque nada é removido das coleções. A recusa de
   identificador duplicado continua sendo a rede de segurança.
5. `formatar_reais` perdeu o truque de três `replace` encadeados para inverter
   separador de milhar e decimal. Os valores em jogo são pequenos e um `replace`
   resolve.
6. A leitura de data aceita só `dd/mm/aaaa`, em vez de tentar três formatos. A
   generalidade extra não servia a ninguém.
7. O `lambda` dentro da tupla `CENARIOS` virou a função `cenario_vazio`.

O que **não** foi simplificado, e por quê: a hierarquia de exceções próprias
(`ErroDeBiblioteca` e as cinco filhas) ficou. É herança, que é conteúdo central de
POO, demonstra o conceito de forma concreta e é a alternativa a falhar em
silêncio. `@dataclass(frozen=True)` também ficou: é o mecanismo de imutabilidade
do projeto e o que sustenta a resposta da questão C.

Verificação após os ajustes: 68 testes passando, nenhum comentário ou docstring,
e o teste de mutação (quebrar o código de propósito para ver se a suíte percebe)
pegou 8 de 10 quebras, sendo as 2 restantes mutações equivalentes, sem efeito
observável.
