# TokenLab-NER
- La tâche à réaliser : token classification
- Le corpus cible : conll2003
- Lien du corpus : https://huggingface.co/datasets/conll2003?row=0
- Types de prédiction : NER (reconnaissance d'entités nommées) tagging, POS tagging, Chunk tagging, tokenisation de phrases et de tokens
- Modèles servis :
  - dslim/bert-base-NER
  - dslim/bert-large-NER
  - flair/ner-english
- Ce corpus procède la classification de tokens en termes de tokenisation, de POS tagging, de chunk tagging et de NER tagging. Comme indiqué dans le nom, c'est un corpus construit en 2003. Il présente un tableau de 5 colonnes. La première colonne liste les ID de chaque phrase des textes. Chaque phrase, étant tokenisée en liste de tokens, occupe une ligne dans la deuxième colonne. Dans la troisième colonne, chaque ligne est une liste d'étiquettes de POS. Chaque POS est représenté par un chiffre unique au lieu de l'étiquette elle-même pour une meilleure visualisation. La convention de la correspondance des étiquettes avec leur chiffres est fournie dans la description du corpus. La quatrième colonne est aussi des listes d'étiquettes sous forme de chiffres. Cette fois-ci, il s'agit des étiquettes de chunk. La dernière colonne présente les listes des entitées nommées, toujours représentées par des chiffres avec la convention de la correspondance fournie dans la description du corpus.
