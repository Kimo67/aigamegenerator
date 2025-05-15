

label node_0:
    "Ceci est le début de notre histoire."
    jump node_128
    return

label node_128:
    show mario happy
    MARIO "Qu'est-ce qui se passe là-haut ? Je sens quelque chose de pas clean"
    show mario angry
    MARIO "Oh non ! Ce n'est vraiment pas rafraîchissant comme atmosphère ici"
    show mario neutral
    MARIO "Quoi qu'il arrive, je vais y aller pour voir ce qui se passe"
    MARIO "Qui est-ce qui parle ? C'est quoi ce bordel ?"
    show mario angry
    MARIO "T'es quoi ce mec qui sort de nulle part avec sa clique ?"
    MARIO "Quel brasage ? Je n'en sais rien du tout ! Arrêtez de me dire des trucs absurdes !"
    jump node_129
    return

label node_129:
    hide mario
    show mario angry
    MARIO "Il a dit quoi ? Je veux pas jouer les idiots ici !"
    show mario angry at left
    show hans neutral at center
    HANS "Pourquoi ne comprenez-vous rien ? Nous venons de l'angelesecteur, le secteur des anges malicieux"
    MARIO "L'angealessecteur, les anges ? Mais c'est n'importe quoi ! Je ne vois pas ça comme ça."
    return
