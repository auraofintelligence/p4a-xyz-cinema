# Portrait lyric videos and titled covers

Implementation reviewed 28 October 2026, Australia/Brisbane.

The homepage now plays the current portrait lyric videos for **The Purple Mat That Could** and **Don't Throw A Brick (Fill A Form)**. Each has a newly titled cover made from its existing portrait artwork. The Musicverse hero uses the same updated Brick video and cover; Purple Mat's track card links to its current portrait video.

The older YouTube embeds were replaced with native players, with playback controls, inline phone playback, full portrait framing and direct video links. Videos load on request. Existing page structure, navigation, civic content and source observation dates are retained.

| Song | Finished export | Website video | Cover |
| --- | --- | --- | --- |
| The Purple Mat That Could | Portrait V3, 1080 × 1920, 247.786 seconds | `assets/media/the-purple-mat-that-could-portrait-v3.mp4` | `assets/media/the-purple-mat-that-could-portrait-cover-v1.jpg` |
| Don't Throw A Brick (Fill A Form) | Portrait V1 with the mat layer, 1080 × 1920, 172.567 seconds | `assets/media/dont-throw-a-brick-fill-a-form-portrait-v1.mp4` | `assets/media/dont-throw-a-brick-fill-a-form-portrait-cover-v1.jpg` |

The website MP4s retain the exact finished H.264 video and AAC audio packets. No lyrics, timing, animation or sound were re-encoded. Only title metadata, attached cover pictures and front-loaded streaming headers were packaged for the website. The source exports and artwork remain unchanged.

Both title covers were visually checked. Both videos played successfully in the browser at their native 1080 × 1920 resolution, without a media error. Desktop 1280-pixel and phone 390-pixel layouts were inspected; neither page overflowed horizontally. Covers retain the full portrait composition. `git diff --check` was checked with the repository's retained CRLF line endings recognised.

The dated media and page-version record is [musicverse-media-2026-10-28.json](../../content/history/musicverse-media-2026-10-28.json). GitHub commit history, the Pages deployment run and the live homepage establish publication separately from these implementation checks.
