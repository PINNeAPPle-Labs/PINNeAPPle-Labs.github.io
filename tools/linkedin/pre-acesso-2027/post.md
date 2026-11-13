# LinkedIn, pré-acesso ao PINNeAPPle Studio

Post de divulgação da lista de pré-acesso. Imagem: `card.jpg` (1200x1200), gerada por
`render.py` a partir de `card.html`.

Escrito para: LinkedIn, público de engenharia (mecânica, CFD, simulação) e de AI aplicada.
Idioma principal: português. A versão em inglês, para o post espelho, está no fim.

---

## Post (PT)

Na prática, a maior parte do tempo de um estudo de simulação não vai para o solver. Vai
para traduzir o problema num caso que roda: escolher o método, montar a malha, descobrir no
terceiro dia que a condição de contorno estava errada.

O PINNeAPPle Studio existe para tirar essa etapa do caminho.

Você escreve o que precisa em português comum ("dissipador de aletas para 60 W"). A
plataforma procura no catálogo uma ferramenta que já resolve aquilo, compara os seus números
com a faixa em que ela foi validada e responde uma de quatro coisas: cobre e roda, falta este
dado, cobre só em parte, ou não cobre. Se roda, volta com o valor, as verificações uma por
uma com valor e limite, a versão do código e o hash de cada arquivo.

Os números de hoje, lidos do próprio catálogo: 10.055 ferramentas catalogadas, 4.987
executáveis de ponta a ponta, 1.693 verificadas contra uma referência. Com o limite na mesma
frase: verificar não é o mesmo que validar para o seu caso, e a plataforma mostra quando o
seu caso cai fora da faixa em que aquela ferramenta foi testada.

O Studio abre em 2027, em prévia fechada. A lista de pré-acesso está aberta agora: quem entra
recebe o convite antes, na ordem de inscrição, e ajuda a decidir o que entra primeiro. São
três perguntas.

→ Pré-acesso: https://forms.gle/FQT8ekYrHBaKizQo8

Até lá, os casos continuam rodando com o nosso time, com escopo fechado e a conta aberta.

#CFD #Simulação #EngenhariaMecânica #GêmeoDigital #PhysicsAI

---

## Versão curta (PT), para quem prefere post de três parágrafos

Uma frase basta para pedir uma simulação no PINNeAPPle Studio: "dissipador de aletas para
60 W". Ele acha no catálogo a ferramenta que resolve, confere se o seu caso cabe na faixa em
que ela foi validada e devolve o número com as verificações ao lado, cada uma com valor e
limite. Se o caso estiver fora da faixa, ele diz, em vez de entregar um campo colorido.

Hoje o catálogo tem 10.055 ferramentas catalogadas, 4.987 executáveis de ponta a ponta e
1.693 verificadas contra uma referência externa. Verificar não é validar para o seu caso, e
o produto mostra a diferença.

O Studio abre em 2027, em prévia fechada. A lista de pré-acesso está aberta, são três
perguntas: https://forms.gle/FQT8ekYrHBaKizQo8

#CFD #Simulação #EngenhariaMecânica #PhysicsAI

---

## Post (EN)

In practice, most of the time in a simulation study does not go to the solver. It goes to
turning the problem into a case that runs: picking the method, building the mesh, finding out
on day three that the boundary condition was wrong.

PINNeAPPle Studio exists to take that step out of the way.

You write what you need in plain language ("fin heatsink for 60 W"). The platform looks up a
tool in the catalogue that already solves it, compares your numbers with the range that tool
was validated in, and answers one of four things: covered, run it; missing one input; partly
covered; or not covered, and why. When it runs, you get the value, the checks one by one with
value and limit, the code version and the hash of every file.

Today's counts, read from the catalogue itself: 10,055 tools catalogued, 4,987 runnable end to
end, 1,693 verified against a reference. With the limit in the same sentence: verified is not
the same as validated for your case, and the platform says so when your case falls outside the
range the tool was tested in.

The Studio opens in 2027, in a closed preview. The early-access list is open now: whoever
joins gets the invite first, in sign-up order, and helps decide what ships first. Three
questions.

→ Early access: https://forms.gle/3F3n132d35N1hWyd6

Until then, cases keep running with our team, with a closed scope and the work shown.

#CFD #Simulation #MechanicalEngineering #DigitalTwin #PhysicsAI

---

## De onde sai cada número

| número | origem |
|---|---|
| 10.055 / 4.987 / 1.693 | faixa `#exist` da home, lida da tela de cobertura do Studio (`img/eng/studio-coverage.webp`) |
| "2027, prévia fechada" | `pre_lead` em `build.py`, o mesmo texto do site |
| quatro respostas | seção `#fluxo`, etapa 02 |
| verificações com valor e limite, versão e hash | seção `#fluxo`, etapa 04 |
| a frase sobre verificar não ser validar | seção `#confianca`, primeiro item |

A primeira linha do post é opinião de engenharia, escrita como tal ("na prática"), não é
número medido. Nenhuma outra afirmação do post é estimativa: todas saem do site ou do
formulário de pré-acesso.
