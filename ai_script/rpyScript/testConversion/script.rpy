define Eileen = Character("Eileen", color="#c8ffc8")
define Bob = Character("Bob", color="#ffc8ff")
define Alice = Character("Alice", color="#c8c8ff")
define Charlie = Character("Charlie", color="#ffffc8")

scene bg_cafe

label start:
    show eileen
    Eileen "Welcome to the café!"
    show eileen  at left
    show bob  at center
    Bob "It's nice to hang out together."
    show eileen  at left
    show bob  at center
    show alice  at right
    Alice "Yeah, it's been a while!"
    hide eileen
    show bob  at center
    show alice  at right
    show charlie  at left
    Charlie "I wasn't expecting to see everyone here!"
    hide bob
    hide alice
    hide charlie
    menu:
        "What should we do?"
        "Order coffee." :
            jump coffee_scene
        "Chat for a while." :
            jump chat_scene
    return

label coffee_scene:
    show eileen
    Eileen "Let's order some coffee."
    show eileen  at left
    show charlie  at center
    Bob "I want some tea!"
    hide eileen
    hide charlie
    jump after_choice
    return

label chat_scene:
    show bob
    Bob "I'd love to catch up with everyone!"
    hide bob
    jump after_choice
    return

label after_choice:
    show alice
    Alice "This was a great idea!"
    show alice  at left
    show charlie  at center
    Charlie "Yeah, we should do this more often."
    hide alice
    hide charlie
    return

label end:
    scene bg_street
    show bob
    Bob "Time to head home."
    return
