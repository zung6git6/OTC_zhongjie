# OTC_zhongjie
- La tâche à réaliser : token classification
- Le corpus cible : Open-Orca/SlimOrca
- Lien du corpus : https://huggingface.co/datasets/Open-Orca/SlimOrca
- Types de prédiction : NER (reconnaissance d'entités nommées), classification de tokens selon lemme, UPOS ou encore dépendance syntaxique.
- Modèles servis :
  - Jackalope 7B : https://huggingface.co/openaccess-ai-collective/jackalope-7b#jackalope-7b
  - OpenOrca - Mistral - 7B - 8k - Slim Data! : https://huggingface.co/Open-Orca/Mistral-7B-SlimOrca
- Ce corpus recueillit les messages transmis à ChatGPT de la part de l'humain et du système et les messages de retour de ChatGPT. Le corpus présente une structure de données sous fomre de listes de dictionnaires (python). Dans chaque liste, il y a trois dictionnaires. Chaque dictionnaire a 3 entrées, la première entrée indique l'expéditeur tels que "system", "human" et "gpt", la deuxième indique les messages d'expéditeurs et la dernière indique une indice de poids "weight". J'ai remarqué que les valeurs de "weight" sont toujours identiques pour chaque expéditeur, "null" pour "system", "0" pour "human" et "1" pour "gpt".
- Ce corpus est en réalité un sous-ensemble tiré du corpus OpenOrca, qui recueillit les conversations de l'être humain avec GPT4. Différent du corpus d'origine OpenOcra, ce corpus a été traité par GPT-4 dans le but d'exclure les réponses incorrectes ou médiocres de GPT4, en s'appuyant sur les annotations humaines de la base de données FLAN. Ce traitement réduit la taille du corpus à environ 500,000 entrées.
