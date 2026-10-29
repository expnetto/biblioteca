# Apoio aos manuscritos

Material de referência para copiar à mão em papel A4 branco sem pautas.
Este arquivo **não** substitui a entrega: o enunciado exige que os dois diagramas
e as cinco respostas sejam feitos inteiramente à mão, com o nome completo em cada
folha. Produzido digitalmente e impresso não é aceito.

**Nome para identificar as folhas:** Eraldo Xavier Pimentel Netto

O código está congelado no commit `6004d76`. Qualquer renomeação posterior
invalida os diagramas abaixo.

---

## 1. Diagrama de Classes (UML)

Quatro caixas. Em cada uma, o nome no topo, os atributos no meio, os métodos
embaixo. `+` para público, `-` para privado.

### Livro  *(imutável, frozen)*
```
- identificador: str
- titulo: str
- autor: str
- categoria: str
```
Responsabilidade: representar um exemplar único do acervo. Não guarda
disponibilidade.

### Usuario  *(imutável, frozen)*
```
- identificador: str
- nome: str
- matricula: str
```
Responsabilidade: representar a pessoa cadastrada.

### Emprestimo  *(imutável, frozen)*
```
- identificador: str
- livro: Livro
- usuario: Usuario
- data_emprestimo: date
- data_prevista_devolucao: date
- data_devolucao: date | None
+ esta_ativo(): bool
+ esta_atrasado(data_referencia): bool
+ dias_de_atraso(data_referencia): int
+ devolvido_em(data): Emprestimo
```
Responsabilidade: representar a retirada de um livro por um usuário e responder
sobre o próprio estado. `devolvido_em` não altera o objeto: devolve um novo.

### Biblioteca  *(mutável)*
```
- _livros: list[Livro]
- _usuarios: list[Usuario]
- _emprestimos: list[Emprestimo]
+ cadastrar_livro(livro): Livro
+ cadastrar_usuario(usuario): Usuario
+ buscar_livro(identificador): Livro
+ buscar_usuario(identificador): Usuario
+ buscar_emprestimo(identificador): Emprestimo
+ livros(): tuple[Livro]
+ usuarios(): tuple[Usuario]
+ emprestimos(): tuple[Emprestimo]
+ registrar_emprestimo(id_livro, id_usuario, data_emprestimo, data_prevista): Emprestimo
+ registrar_devolucao(id_emprestimo, data_devolucao): Emprestimo
+ proximo_identificador_de_livro(): str
+ proximo_identificador_de_usuario(): str
+ relatorio_de_multas(data_referencia): RelatorioMultas
+ estatisticas(data_referencia): Estatisticas
```
Responsabilidade: ser a única guardiã de estado mutável do sistema, controlar as
operações de gerenciamento e disponibilizar os dados de relatórios e estatísticas.

### Relacionamentos e multiplicidades

```
Biblioteca  1 ──────── 0..*  Livro          (agregacao: o acervo)
Biblioteca  1 ──────── 0..*  Usuario        (agregacao: a comunidade)
Biblioteca  1 ──────── 0..*  Emprestimo     (composicao: nascem e morrem com ela)

Usuario     1 ──────── 0..*  Emprestimo     (um usuario tem vários empréstimos)
Livro       1 ──────── 0..*  Emprestimo     (histórico; no máximo 1 ativo por vez)
```

Anote ao lado da associação `Livro–Emprestimo`: **no máximo um empréstimo ativo
por livro em um dado momento** (regra 2). O histórico pode ter vários, mas apenas
um sem `data_devolucao`.

---

## 2. Diagrama de Fluxo de Processamento Funcional

Fluxo da geração do relatório de multas. Sete blocos ligados por setas de cima
para baixo. Cada bloco leva as cinco informações exigidas.

```
┌─────────────────────────────────────────────────────────┐
│ cli.exibir_relatorio_de_multas                          │
│ recebe: entrada digitada pelo usuario                   │
│ produz: data_referencia (date)                          │
│ IMPURA  (input)                                         │
│ operacao funcional: nenhuma                             │
└───────────────────────┬─────────────────────────────────┘
                        v
┌─────────────────────────────────────────────────────────┐
│ Biblioteca.relatorio_de_multas                          │
│ recebe: data_referencia                                 │
│ produz: tuple[Emprestimo] (copia do estado interno)     │
│ IMPURA  (le estado mutavel de self._emprestimos)        │
│ operacao funcional: nenhuma                             │
└───────────────────────┬─────────────────────────────────┘
                        v
┌─────────────────────────────────────────────────────────┐
│ multas.emprestimos_atrasados                            │
│ recebe: tuple[Emprestimo], data_referencia              │
│ produz: tuple[Emprestimo] apenas ativos e vencidos      │
│ PURA                                                    │
│ operacao funcional: FILTER                              │
└───────────────────────┬─────────────────────────────────┘
                        v
┌─────────────────────────────────────────────────────────┐
│ multas.multa_do_emprestimo  (aplicada a cada item)      │
│ recebe: Emprestimo, data_referencia, valor_diario       │
│ produz: ItemMulta (emprestimo, dias_de_atraso, valor)   │
│ PURA    chama calcular_multa → PURA                     │
│ operacao funcional: MAP                                 │
└───────────────────────┬─────────────────────────────────┘
                        v
┌─────────────────────────────────────────────────────────┐
│ soma dos valores                                        │
│ recebe: tuple[ItemMulta], acumulador inicial 0.0        │
│ produz: total (float)                                   │
│ PURA                                                    │
│ operacao funcional: REDUCE                              │
└───────────────────────┬─────────────────────────────────┘
                        v
┌─────────────────────────────────────────────────────────┐
│ RelatorioMultas  (dataclass frozen)                     │
│ recebe: data_referencia, itens, total                   │
│ produz: estrutura imutavel de saida                     │
│ PURA                                                    │
│ operacao funcional: nenhuma                             │
└───────────────────────┬─────────────────────────────────┘
                        v
┌─────────────────────────────────────────────────────────┐
│ cli.exibir_relatorio_de_multas  (impressao)             │
│ recebe: RelatorioMultas                                 │
│ produz: texto no terminal                               │
│ IMPURA  (print)                                         │
│ operacao funcional: nenhuma                             │
└─────────────────────────────────────────────────────────┘
```

Ao copiar, marque explicitamente a origem dos dados no segundo bloco e a saída no
último: o enunciado pede que entradas e saídas estejam identificadas, além da
classificação pura/impura e da operação funcional de cada etapa.

---

## 3. As cinco questões

O que segue é o conteúdo, não o texto a decorar. Escreva com suas palavras.

### A) Função pura implementada e por que tem transparência referencial

Função: `calcular_multa(dias_atraso, valor_diario)`, em `biblioteca/multas.py`.

```python
def calcular_multa(dias_atraso: int, valor_diario: float) -> float:
    if dias_atraso <= 0:
        return 0.0
    return dias_atraso * valor_diario
```

Tem transparência referencial porque a chamada pode ser substituída pelo seu
resultado em qualquer ponto do programa sem alterar o comportamento:
`calcular_multa(5, 2.00)` e `10.0` são intercambiáveis, sempre e em qualquer
ordem de execução. Isso vale por três motivos: ela depende **apenas** dos dois
parâmetros recebidos, não lê nada de fora (nem variável global, nem relógio, nem
estado de objeto, nem entrada do usuário); não escreve nada em lugar nenhum (não
imprime, não altera os argumentos, não grava); e não tem memória entre chamadas.
Repare que o valor diário é **parâmetro**, não a constante `VALOR_MULTA_DIARIA`
lida por dentro — se a função consultasse a constante, uma mudança nela mudaria o
resultado da mesma chamada, e a transparência se perderia. O teste
`test_multa_tem_transparencia_referencial` afirma exatamente essa propriedade.

### B) Operação impura e por que não é função pura

Operação: `Biblioteca.registrar_emprestimo`, em `biblioteca/biblioteca.py`.

Não é pura por três razões independentes, e qualquer uma bastaria:

1. **Altera estado externo à chamada.** A última coisa que faz é
   `self._emprestimos.append(emprestimo)`, mutando uma lista que vive no objeto e
   sobrevive ao retorno.
2. **O resultado depende de estado que não foi passado como argumento.** A mesma
   chamada com os mesmos parâmetros tem sucesso na primeira vez e levanta
   `LivroIndisponivelError` na segunda, porque depende de `self._emprestimos`.
   Não há transparência referencial: a chamada não pode ser trocada pelo seu
   resultado.
3. **Gera o identificador a partir do estado atual.** O identificador vem de
   `proximo_identificador("E", len(self._emprestimos))`: devolve `E1`, depois
   `E2`, conforme a quantidade já registrada. A função `proximo_identificador`
   em si é pura — quem é impuro é o método, que lê `self._emprestimos` para
   saber o que passar a ela.

Outro exemplo bom de citar é o `cli.py` inteiro, que é o único lugar do projeto
com `input()` e `print()` — entrada e saída são efeitos colaterais por definição,
já que dependem do mundo externo e o modificam. As fábricas de `cenarios.py`
também são impuras, porque instanciam uma `Biblioteca` e chamam os métodos que
mutam estado.

### C) Como a imutabilidade foi aplicada e o que ela evita

Quatro mecanismos concretos:

1. **Entidades congeladas.** `Livro`, `Usuario` e `Emprestimo` são
   `@dataclass(frozen=True)`. Tentar `livro.titulo = "outro"` levanta
   `FrozenInstanceError`. Não é convenção nem disciplina do programador: a
   linguagem recusa.
2. **Devolução sem mutação.** `Emprestimo.devolvido_em(data)` constrói e devolve
   um **objeto novo**, copiando os campos do original e preenchendo só a data de
   devolução.
   O empréstimo original continua existindo intacto; a `Biblioteca` troca a
   referência na sua lista. Isso preserva o histórico e torna impossível
   "desdevolver" por acidente.
3. **Saídas em tupla.** Todas as funções puras e todos os métodos de consulta da
   `Biblioteca` devolvem `tuple`, não `list`. Quem recebe não consegue alterar o
   resultado nem, por tabela, o estado interno da biblioteca.
4. **Acumulador não mutado no `reduce`.** Nas estatísticas, cada passo cria um
   dicionário novo com `{**contagem, chave: contagem.get(chave, 0) + 1}` em vez
   de `contagem[chave] += 1`.

Problemas que isso evita: **aliasing**, em que dois trechos guardam a mesma lista
e um altera o que o outro está lendo; **efeito colateral à distância**, em que uma
função de consulta modifica dados de quem a chamou (o enunciado proíbe isso na
§5.6); **estado inconsistente intermediário**, porque não existe um objeto
parcialmente atualizado — ou o novo valor existe inteiro, ou não existe; e
**dificuldade de teste**, já que uma função que não altera a entrada pode ser
chamada quantas vezes quiser, na ordem que for, com o mesmo resultado. Em
concorrência, elimina a classe inteira de corrida de dados sobre leitura e
escrita simultâneas no mesmo objeto — mas não resolve tudo, como a questão E
mostra.

### D) Comparação entre a versão imperativa e a funcional

Base: `biblioteca/comparacao.py`, com `total_de_multas_funcional` e
`total_de_multas_imperativo`.

**Legibilidade.** A funcional é lida em três etapas nomeadas — filtrar os
atrasados, converter cada um em valor, somar — e diz *o que* se quer. A
imperativa diz *como*: abre um laço, aninha dois `if` e vai somando, misturando
seleção, cálculo e agregação no mesmo bloco. Para descobrir o que a imperativa
faz, é preciso simular o laço mentalmente.

**Manutenção.** A imperativa repete por dentro a regra de atraso
(`data_devolucao is None` e `data_prevista_devolucao < data_referencia`), que na
funcional vem de `esta_atrasado`. Essa duplicação é o problema de manutenção
concreto: se a regra mudar — digamos, passar a haver carência de dois dias — a
funcional muda em um lugar e a imperativa em outro, e as duas silenciosamente
discordam. Na funcional, cada etapa é testável isoladamente; na imperativa, só o
resultado final é testável.

**Mutabilidade.** A imperativa depende de uma variável reatribuída a cada volta
(`total = total + ...`), que passa por vários valores intermediários incorretos
antes de chegar ao certo. A funcional não tem variável reatribuída: o
`reduce` encadeia valores novos e nenhum nome é redefinido.

**Efeitos colaterais.** Nenhuma das duas tem efeito colateral externo — ambas só
leem a coleção recebida e devolvem um número. A diferença não é a presença de
efeito, é a presença de **estado mutável interno**. A imperativa carrega um; a
funcional, nenhum. É o que torna a funcional trivialmente paralelizável e a
imperativa não.

**Equivalência.** `test_as_duas_versoes_concordam_em_todos_os_cenarios` verifica
a igualdade nos três cenários povoados e em quatro datas de referência, mais os
casos de borda: coleção vazia, ninguém atrasado, todos atrasados, devolvido com
atraso.

### E) Dois usuários emprestando o mesmo livro ao mesmo tempo

**O problema.** `registrar_emprestimo` faz uma verificação seguida de uma ação:
primeiro consulta `esta_disponivel(livro, self.emprestimos())`, depois executa
`self._emprestimos.append(...)`. É um **check-then-act**, e a janela entre os dois
passos é a vulnerabilidade. Com dois fluxos simultâneos, ambos podem consultar
antes de qualquer um gravar, ambos concluem que o livro está livre, e ambos
gravam. O resultado é dois empréstimos ativos do mesmo exemplar — exatamente o
que a regra 2 proíbe —, e o sistema sequer percebe, porque cada operação, vista
isoladamente, respeitou a regra. É uma condição de corrida, e é também a razão
pela qual essa invariante não pode ser verificada só na entrada da função.

**Funções puras e imutabilidade bastam? Não.** E a justificativa é a parte que
importa: elas resolvem um problema diferente do que está em jogo aqui.

O que elas resolvem é a **corrida de dados** — dois fluxos escrevendo na mesma
posição de memória e corrompendo o valor. Com entidades congeladas e funções que
devolvem estruturas novas, isso desaparece: ninguém pode alterar um `Emprestimo`
que outro fluxo está lendo, e `esta_disponivel` pode ser avaliada em paralelo sem
risco, porque não toca em nada.

O que elas **não** resolvem é a **condição de corrida sobre a decisão**. O
problema não é a memória se corromper; é que a decisão de emprestar foi tomada
com base numa foto do estado que deixou de ser verdadeira antes da gravação. A
pureza garante que `esta_disponivel` responda corretamente **sobre a coleção que
recebeu** — e ela faz isso. O defeito está em outro lugar: na suposição de que
aquela coleção continuava atual no instante do `append`. Nenhuma propriedade de
uma função pura pode garantir isso, porque a garantia necessária é sobre
**ordenação entre operações**, não sobre o cálculo de cada uma.

**O que resolveria.** Tornar a sequência verificar-e-gravar **atômica**: ou um
lock em volta do trecho que muta a `Biblioteca`, ou serializar os empréstimos em
uma única fila, ou — no caso de banco de dados — uma transação com restrição de
unicidade que impeça dois empréstimos ativos do mesmo livro, deixando o banco
rejeitar o segundo. A observação de projeto é que a imutabilidade **ajuda**: por
concentrar toda a mutação em um único ponto (a `Biblioteca`), ela reduz o trecho
que precisa de proteção a poucas linhas, em vez de espalhar o risco pelo sistema.
Ela torna o problema localizável e barato de corrigir — mas quem corrige é o
mecanismo de sincronização, não a pureza.
