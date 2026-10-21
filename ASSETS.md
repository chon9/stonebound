# Original game artwork

Generated with the built-in imagegen tool on 21 October 2026. These are original illustrations for Stonebound; they are not claimed as third-party CC0 artwork. No Hikaru no Go character or franchise art is used.

- City: `web/assets/aoharu.png`
- Four-character atlas: `web/assets/cast.png`; each portrait is selected through CSS background positioning.
- Boards, stones, favicon, and UI icons: drawn in code with canvas, CSS, or SVG.

## City prompt

Use case: illustration-story. Asset type: background artwork for an original cozy anime Go adventure game named Stonebound. Create a beautiful richly detailed wide landscape 1536x1024, hand-painted anime background of a nostalgic Japanese riverside town in late spring. Elevated three-quarter view across canal toward a charming old wooden Go club with tiled roof and warm paper lanterns, small bridge, stone steps, narrow shopping lane, cherry blossom trees, forested hills, a distant train crossing, sunlit golden afternoon with soft floating petals. Painterly watercolor textures, cinematic environment art, tasteful warm cream and sage green and coral peach palette, exquisite architectural detail. No people in foreground, no lettering, no logos, no UI, no text, no watermark. Original place, no franchise references. Composition with canal in lower half, buildings in middle, sky upper quarter. This will be a full-bleed game city exploration scene.

## Character atlas prompt

Use case: illustration-story. Asset type: original anime game character portrait atlas, exactly FOUR equally sized vertical panels side by side in a wide landscape 1536x1024 image, no gutters. Each panel shows one distinct waist-up original anime character on a simple warm muted cream background. Panel 1: friendly teenage boy with tousled chestnut brown hair, amber eyes, open cream jacket and sage green shirt, warm relaxed smile. Panel 2: confident young woman with short dark teal bob hair, hazel eyes, pale linen shirt and terracotta apron, hand on hip, cheerful. Panel 3: serious male young adult with black blue hair, slim glasses, navy school jacket over white shirt, cool reserved expression. Panel 4: kind silver haired older man with tied hair, light stubble, moss green traditional haori, wise gentle smile. Clean hand drawn anime linework, delicate watercolor shading, beautiful expressive eyes, cozy grounded coming-of-age game visual novel art. All heads fully visible with generous top margins and similarly placed. No text, no lettering, no borders, no logos, no watermark, no recognizable existing franchise characters.


## Expanded campaign artwork

Five additional four-character atlases (`web/assets/cast-02.png` through `cast-06.png`) provide 20 original portraits. Eight six-panel atlases (`web/assets/comics/chapter-01.png` through `chapter-08.png`) provide 48 original manga illustrations. The top three panels form each chapter’s arrival, and the bottom three form its conclusion.

All 13 generation prompts are recorded verbatim in `content/art-prompts.json`; `scripts/build-art-briefs.py` maintains those briefs. These assets were generated with the built-in imagegen tool for this project. They are not third-party CC0 downloads. Dialogue and captions are authored separately in `stonebound/story.py` and are never baked into images. Material appearances are authored in `web/skins.js`, shared by previews and actual matches.

Chapter 8 was corrected after visual review: the keepsake close-up shows an empty Go board, and the final match has exactly two active players with friends observing. The image-edit brief is recorded in `content/art-corrections.json`.

## Ghost-master artwork

Generated with the built-in imagegen tool on 22 October 2026: `web/assets/sensei.png` is Yangui / 砚归’s transparent portrait, and `web/assets/comics/sensei.png` contains six original panels for two spirit-story episodes. Exact prompts are in `content/sensei-art-prompts.json`. The character and narrative are original; these generated assets are not third-party CC0 downloads. Bilingual dialogue is authored in `stonebound/sensei.py`.
