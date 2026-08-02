# Wordle CLI — Architecture

## Module Structure

The project is split into four packages plus a thin entry point. Each package has a single responsibility and dependencies only flow inward toward `game/`.

```mermaid
graph TD
    main["main.py\nEntry point & game loop"]

    subgraph words["words/"]
        W["words.py\nload_word_list()\nis_valid_guess()"]
    end

    subgraph game["game/"]
        E["engine.py\nscore_guess()\nmake_guess()\nis_game_over()"]
    end

    subgraph cli["cli/"]
        R["renderer.py\nrender()\nrender_legend()\nbuild_keyboard_state()"]
    end

    subgraph persistence["persistence/"]
        S["stats.py\nload_stats()\nsave_stats()\nupdate_stats()"]
        D["daily.py\nget_daily_answer()\nalready_played_today()\nrecord_daily_result()"]
    end

    main --> W
    main --> E
    main --> R
    main --> S
    main --> D
    R --> E
```

---

## Data Structures

The core data types that flow through the game.

```mermaid
classDiagram
    class LetterResult {
        <<enumeration>>
        CORRECT
        PRESENT
        ABSENT
    }

    class GameState {
        +str answer
        +list~str~ guesses
        +list~list~LetterResult~~ results
        +str status
    }

    class Stats {
        +int schema_version
        +int games_played
        +int wins
        +int current_streak
        +int max_streak
        +str daily_last_played
        +str daily_last_result
    }

    GameState --> LetterResult : results contain
```

---

## Game Loop Flow

How a single game plays out from launch to result.

```mermaid
flowchart TD
    A([python3 main.py]) --> B{--daily flag?}
    B -- Yes --> C{Already played\ntoday?}
    C -- Yes --> D[Show previous result\nand exit]
    C -- No --> E[Pick today's word\nvia epoch index]
    B -- No --> F[Pick random word\nfrom answers.txt]
    E --> G
    F --> G

    G[Create GameState] --> H[render board]
    H --> I[Prompt for guess]
    I --> J{Valid input?}
    J -- QUIT/EXIT --> K[Save stats\nThanks for playing!]
    J -- Wrong length\nor not in list --> I
    J -- Valid word --> L[score_guess\nmake_guess]
    L --> M{Game over?}
    M -- No, guesses left --> H
    M -- Won --> N[render final board]
    M -- Lost, 6 guesses used --> N
    N --> O[update_stats\nsave_stats]
    O --> P[Show result\n+ stats line]
    P --> Q{Play again?\ny/n}
    Q -- Yes --> G
    Q -- No --> R([Exit])
```

---

## Guess Scoring Algorithm

The two-pass algorithm inside `score_guess()` that handles duplicate letters correctly.

```mermaid
flowchart TD
    A["score_guess(guess, answer)"] --> B[Initialise result = ABSENT × 5\nanswer_remaining = list of answer chars]

    B --> C["Pass 1 — lock greens\nFor each position i:\nif guess[i] == answer[i]"]
    C --> D["result[i] = CORRECT\nanswer_remaining[i] = None"]
    D --> E[Next position]
    E --> C
    C -- All positions done --> F

    F["Pass 2 — assign yellows\nFor each position i:\nif result[i] == CORRECT → skip"]
    F --> G{"guess[i] in\nanswer_remaining?"}
    G -- Yes --> H["result[i] = PRESENT\nRemove first match\nfrom answer_remaining"]
    G -- No --> I[result[i] stays ABSENT]
    H --> J[Next position]
    I --> J
    J --> F
    F -- All positions done --> K([Return result list])
```

---

## Persistence Layer

How stats are read and written to disk.

```mermaid
sequenceDiagram
    participant M as main.py
    participant S as stats.py
    participant D as daily.py
    participant FS as ~/.wordle-cli/stats.json

    M->>S: load_stats()
    S->>FS: Read file (or return defaults)
    FS-->>S: JSON dict
    S-->>M: stats dict

    Note over M: Game plays out...

    M->>S: update_stats(stats, won=True)
    S-->>M: updated stats dict (copy)

    opt Daily mode
        M->>D: record_daily_result(stats, "won")
        D-->>M: stats with daily fields set
    end

    M->>S: save_stats(stats)
    S->>FS: Write to stats.tmp
    S->>FS: os.replace(tmp → stats.json)
```

---

## Rendering Pipeline

How `GameState` becomes terminal output each turn.

```mermaid
flowchart LR
    GS[GameState] --> R[render]

    R --> CC{Color\nsupported?}

    CC -- Yes --> CL[Clear terminal\nANSI codes]
    CC -- No --> PT[Plain text\nbracket tiles]

    CL --> GB[Draw 6-row\nguess grid\ncolored tiles]
    PT --> GB

    GB --> KB[build_keyboard_state\nPriority: CORRECT > PRESENT > ABSENT]
    KB --> KD[Draw QWERTY\nkeyboard rows\ncolored by best state]
    KD --> LD[render_legend\nCorrect / Present / Absent key]
    LD --> OUT([Terminal output])
```
