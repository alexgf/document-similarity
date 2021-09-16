# Avaliação de Similaridade Entre Documentos Normativos

#### Aluno: [Alexandre Gomes Ferriera](https://github.com/alexgf).
#### Orientador: [Leonardo Forero Mendoza](https://github.com/leofome8).
#### Co-orientador: [Cristian Muñoz](https://github.com/crismunoz).

---

Trabalho apresentado ao curso [BI MASTER](https://ica.puc-rio.ai/bi-master) como pré-requisito para conclusão de curso e obtenção de crédito na disciplina "Projetos de Sistemas Inteligentes de Apoio à Decisão".

- [Link para o código](https://github.com/alexgf/document-similarity).

---

### Resumo

Empresas atualmente lidam com uma crescente quantidade de requisitos regulatórios. Monitorar alterações regulatórias e garantir a conformidade normativa exige análise de uma grande quantidade de documentos e gera um alto custo administrativo. Para auxiilar neste processo, este trabalho pretende indicar quais os documentos mais similares a novos regulamentos, sendo potenciais candidatos para revisão.

Este trabalho tem por objetivo avaliar a utilização de técnicas de Processamento de Linguagem Natural para auxiliar na revisão normativa decorrente de alterações impostas por agencias regulatórias. Para realizar esta avaliação foram obtidas, através de ferramentas de web scrapping, documentos de duas instituições: uma agência reguladora e um banco federal. Estes documentos foram préprocessados, foi feita a lemmatização com auxílio da biblioteca spaCy, a extração de tópicos e criação de word embeddings Word2Vec e TF-IDF foram realizados utilizando-se a biblioteca Gensim. Esses embeddings são utilizados para avaliar similaridade entre novos regulamentos e documentos do base existente utilizando-se similaridade por cosseno.

### Abstract 

Companies nowadays deal with an increasing amount of regulatory requirements. Monitoring regulatory changes and ensuring regulatory compliance requires reviewing a large amount of documents and generates a high administrative cost. To assist in this process, this work intends to indicate which documents are the most similars to new regulations, being potential candidates for revision.

This work aims to evaluate the use of Natural Language Processing techniques to assist in regulations review resulting from changes imposed by regulatory agencies. For this assessment documents from two institutions, a regulatory agency and a federal, bank were obtained through web scraping tools. These documents were pre-processed, lemmatized supported by spaCy library, topics extraction and word embeddings Word2Vec and TF-IDF creations were performed using the Gensim library. These embeddings are used to assess similarity between new regulations and existing base documents using cosine similarity.

---

Matrícula: 191.671.029

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Business Intelligence Master*
