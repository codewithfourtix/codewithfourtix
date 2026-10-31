<!-- upstream:start -->
## Open source

<a href="https://github.com/search?q=is%3Apr+author%3Acodewithfourtix+is%3Apublic&type=pullrequests">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/codewithfourtix/codewithfourtix/main/assets/upstream-dark.svg">
    <img alt="Merged upstream. xAI: Made xAI&#x27;s Python SDK compatible with protobuf 7. Pull requests: xai-sdk-python #223. Google DeepMind: Fixed an out-of-bounds memory write in OpenSpiel&#x27;s Dou Dizhu game. Pull requests: concordia #276 #299 #300, open_spiel #1602. boltons: Fixed 9 bugs in boltons, from list slicing to seeking in JSONL streams. Pull requests: 9 pull requests. AboutCode: Fixed license scans missing Chinese and Japanese license texts. Pull requests: scancode-toolkit #4781 #5343. In review. NVIDIA: Stopped garak&#x27;s AI safety judge from losing the question it was grading. Pull requests: garak #2383, NVTX #181. Microsoft: Fixed NVIDIA model settings crashing every request in Semantic Kernel. Pull requests: knack #309, semantic-kernel #14698. OpenAI: Fixed finished fine-tuning jobs still showing Running in the .NET SDK. Pull requests: whisper #2846 #2847, openai-dotnet #1456, tiktoken #611. Google: Stopped Gemini CLI losing tool results when it recovers from a loop. Pull requests: etils #831, gemini-cli #29871, python-fire #704. Anthropic: Let developers clear a tool&#x27;s description in Anthropic&#x27;s Python SDK. Pull requests: anthropic-sdk-python #1913. Hugging Face: Let evaluate save results on machines without Git installed. Pull requests: evaluate #808 #809." src="https://raw.githubusercontent.com/codewithfourtix/codewithfourtix/main/assets/upstream-light.svg" width="100%">
  </picture>
</a>

Mostly bug fixes in projects I actually use.

<details>
<summary><b>Every upstream pull request</b> (74)</summary>

| Status | Repository | Pull request |
| :--- | :--- | :--- |
| merged | aboutcode-org/scancode-toolkit | [#5343](https://github.com/aboutcode-org/scancode-toolkit/pull/5343) Pin binaryornot back to 0.4.4 |
| merged | aboutcode-org/scancode-toolkit | [#4781](https://github.com/aboutcode-org/scancode-toolkit/pull/4781) Remove duplicate '/project.clj' key in _MANIFEST_ENDS dict |
| merged | aounkazmi-dev/Car-Show-Speed | [#1](https://github.com/aounkazmi-dev/Car-Show-Speed/pull/1) Update: Uploading my phases |
| merged via Copybara | google-deepmind/concordia | [#300](https://github.com/google-deepmind/concordia/pull/300) Allow component comparisons without skip_keys |
| merged via Copybara | google-deepmind/concordia | [#299](https://github.com/google-deepmind/concordia/pull/299) Honor remove_duplicates when searching nested data |
| merged | google-deepmind/concordia | [#276](https://github.com/google-deepmind/concordia/pull/276) Fix typos in document docstrings and package description |
| merged by a maintainer | google-deepmind/open_spiel | [#1602](https://github.com/google-deepmind/open_spiel/pull/1602) Fix out-of-bounds write in dou_dizhu when nobody wins the auction |
| merged | mahmoud/boltons | [#472](https://github.com/mahmoud/boltons/pull/472) Keep the stop barrel valid during cross-barrel deletion |
| merged | mahmoud/boltons | [#471](https://github.com/mahmoud/boltons/pull/471) Normalize BarrelList slice bounds and reverse steps |
| merged | mahmoud/boltons | [#469](https://github.com/mahmoud/boltons/pull/469) Support aware datetimes when relative time defaults to now |
| merged | mahmoud/boltons | [#468](https://github.com/mahmoud/boltons/pull/468) Preserve empty Bits across binary and byte conversions |
| merged | mahmoud/boltons | [#467](https://github.com/mahmoud/boltons/pull/467) Handle zero interquartile range in automatic histograms |
| merged | mahmoud/boltons | [#465](https://github.com/mahmoud/boltons/pull/465) Accept the documented end position in JSONLIterator |
| merged | mahmoud/boltons | [#464](https://github.com/mahmoud/boltons/pull/464) Support relative seeking in binary JSONL streams |
| merged | sipeed/picoclaw | [#608](https://github.com/sipeed/picoclaw/pull/608) docs: fix typos, broken links and inconsistencies in README |
| merged | theajmalrazaq/superflex | [#24](https://github.com/theajmalrazaq/superflex/pull/24) fix(ui): add pointer cursors to interactive elements for better UX |
| merged | xai-org/xai-sdk-python | [#223](https://github.com/xai-org/xai-sdk-python/pull/223) Allow protobuf 7 |
| merged | zeroclaw-labs/zeroclaw | [#1296](https://github.com/zeroclaw-labs/zeroclaw/pull/1296) docs: fix OAuth wording, binary size format, E.164 phone prefix, and … |
| co-authored in [#481](https://github.com/mahmoud/boltons/pull/481) | mahmoud/boltons | [#466](https://github.com/mahmoud/boltons/pull/466) Keep text streams usable after reverse iteration |
| co-authored in [#481](https://github.com/mahmoud/boltons/pull/481) | mahmoud/boltons | [#463](https://github.com/mahmoud/boltons/pull/463) Honor the encoding when reading lines in reverse |
| open | aboutcode-org/commoncode | [#110](https://github.com/aboutcode-org/commoncode/pull/110) Scale fractional timestamp seconds to microseconds |
| open | aboutcode-org/commoncode | [#109](https://github.com/aboutcode-org/commoncode/pull/109) Raise URNValidationError for truncated URNs |
| open | aboutcode-org/fetchcode | [#215](https://github.com/aboutcode-org/fetchcode/pull/215) Follow Bitbucket tag pages when collecting package releases |
| open | aboutcode-org/fetchcode | [#214](https://github.com/aboutcode-org/fetchcode/pull/214) Fetch NuGet registration pages when versions are not inlined |
| open | aboutcode-org/fetchcode | [#213](https://github.com/aboutcode-org/fetchcode/pull/213) Filter Composer development versions by their version value |
| open | aboutcode-org/fetchcode | [#212](https://github.com/aboutcode-org/fetchcode/pull/212) Skip missing upload timestamps when finding PyPI release dates |
| open | aboutcode-org/fetchcode | [#211](https://github.com/aboutcode-org/fetchcode/pull/211) Read npm licenses from the selected release |
| open | aboutcode-org/fetchcode | [#209](https://github.com/aboutcode-org/fetchcode/pull/209) Handle absent CocoaPods versions and homepage metadata |
| open | aboutcode-org/fetchcode | [#208](https://github.com/aboutcode-org/fetchcode/pull/208) Handle GitHub tags whose targets have no commit date |
| open | aboutcode-org/fetchcode | [#207](https://github.com/aboutcode-org/fetchcode/pull/207) Use CocoaPods source tags without changing package versions |
| open | aboutcode-org/fetchcode | [#206](https://github.com/aboutcode-org/fetchcode/pull/206) Match CocoaPods names exactly when reading version lists |
| open | aboutcode-org/fetchcode | [#205](https://github.com/aboutcode-org/fetchcode/pull/205) Preserve prerelease suffixes when normalizing GitHub tags |
| open | aboutcode-org/fetchcode | [#204](https://github.com/aboutcode-org/fetchcode/pull/204) Keep GitHub package tags with no release date |
| open | aboutcode-org/license-expression | [#137](https://github.com/aboutcode-org/license-expression/pull/137) Return warnings for duplicate and empty license aliases |
| open | aboutcode-org/license-expression | [#136](https://github.com/aboutcode-org/license-expression/pull/136) Recheck remaining tokens after removing an overlapping match |
| open | aboutcode-org/license-expression | [#135](https://github.com/aboutcode-org/license-expression/pull/135) Normalize relation case when combining license expressions |
| open | aboutcode-org/python-inspector | [#271](https://github.com/aboutcode-org/python-inspector/pull/271) Remove exact archive suffixes when locating extracted sdists |
| open | aboutcode-org/python-inspector | [#270](https://github.com/aboutcode-org/python-inspector/pull/270) Preserve case and quoted spaces in dependency requirements |
| open | aboutcode-org/python-inspector | [#269](https://github.com/aboutcode-org/python-inspector/pull/269) Do not treat wildcard requirements as exact version pins |
| open | aboutcode-org/scancode-toolkit | [#5260](https://github.com/aboutcode-org/scancode-toolkit/pull/5260) Fix pdf text extraction multipage |
| open | aboutcode-org/scancode-toolkit | [#4786](https://github.com/aboutcode-org/scancode-toolkit/pull/4786) Fix end_line incorrectly assigned from start_line in CSV output #4785 |
| open | aboutcode-org/scancode-toolkit | [#4784](https://github.com/aboutcode-org/scancode-toolkit/pull/4784) Fix empty range in terminate_pool_with_backoff making it a no-op |
| open | aboutcode-org/scancode-toolkit | [#4783](https://github.com/aboutcode-org/scancode-toolkit/pull/4783) Fix incorrect timing parameter passed to run_scanners |
| open | aboutcode-org/scancode-toolkit | [#4782](https://github.com/aboutcode-org/scancode-toolkit/pull/4782) Fix unreachable JSON validation code in validate_input_path |
| open | aboutcode-org/scancode.io | [#2253](https://github.com/aboutcode-org/scancode.io/pull/2253) Clone GitHub and GitLab repository URLs given as inputs |
| open | anthropics/anthropic-sdk-python | [#1913](https://github.com/anthropics/anthropic-sdk-python/pull/1913) fix(tools): preserve an explicitly empty description |
| open | google-deepmind/optax | [#1716](https://github.com/google-deepmind/optax/pull/1716) Fix ACProp second moment to use the new first moment |
| open | google-deepmind/optax | [#1715](https://github.com/google-deepmind/optax/pull/1715) Fix incorrect (1 - b2) coefficient in scale_by_adan |
| open | google-deepmind/regress-lm | [#139](https://github.com/google-deepmind/regress-lm/pull/139) docs: fix broken Extended Usage navigation link in README |
| open | google-gemini/gemini-cli | [#29871](https://github.com/google-gemini/gemini-cli/pull/29871) fix(core): keep the unsent request when loop recovery starts before a turn |
| open | google/etils | [#831](https://github.com/google/etils/pull/831) fix(epath): preserve cloud URI schemes in fsspec walks |
| open | google/python-fire | [#704](https://github.com/google/python-fire/pull/704) Preserve template arguments that contain unhashable literals |
| open | huggingface/evaluate | [#809](https://github.com/huggingface/evaluate/pull/809) Recognize existing directories with dots when saving results |
| open | huggingface/evaluate | [#808](https://github.com/huggingface/evaluate/pull/808) Allow saving evaluation results when Git is not installed |
| open | microsoft/knack | [#309](https://github.com/microsoft/knack/pull/309) Preserve UTF-8 config values when updating settings |
| open | microsoft/semantic-kernel | [#14698](https://github.com/microsoft/semantic-kernel/pull/14698) Python: Send the NVIDIA nvext setting in extra_body |
| open | NVIDIA/garak | [#2383](https://github.com/NVIDIA/garak/pull/2383) Keep the request when truncating judge prompts |
| open | NVIDIA/NVTX | [#181](https://github.com/NVIDIA/NVTX/pull/181) Python: preserve target script arguments in the profiling CLI |
| open | openai/openai-dotnet | [#1456](https://github.com/openai/openai-dotnet/pull/1456) Refresh all FineTuningJob properties in UpdateStatus(RequestOptions) |
| open | openai/tiktoken | [#611](https://github.com/openai/tiktoken/pull/611) Fix concurrent cache initialization on Windows |
| open | openai/whisper | [#2847](https://github.com/openai/whisper/pull/2847) Escape timestamp arrows in word-level subtitles |
| open | openai/whisper | [#2846](https://github.com/openai/whisper/pull/2846) Keep each transcript segment on one TSV row |
| open | package-url/packageurl-python | [#237](https://github.com/package-url/packageurl-python/pull/237) Skip Swift archive URLs when namespace or version is missing |
| open | package-url/packageurl-python | [#236](https://github.com/package-url/packageurl-python/pull/236) Preserve package names inside npm prerelease versions |
| open | package-url/packageurl-python | [#235](https://github.com/package-url/packageurl-python/pull/235) Avoid crashing on Go package URLs without a version |
| open | RocketChat/Rocket.Chat | [#41030](https://github.com/RocketChat/Rocket.Chat/pull/41030) fix: Encrypted toggle ignored when creating a discussion |
| open | RocketChat/Rocket.Chat | [#41028](https://github.com/RocketChat/Rocket.Chat/pull/41028) i18n: Fix spelling errors in English source strings |
| open | sgl-project/sglang | [#28845](https://github.com/sgl-project/sglang/pull/28845) Fix Llama32 tool-call parser truncating text after final call |
| closed | aboutcode-org/fetchcode | [#210](https://github.com/aboutcode-org/fetchcode/pull/210) Preserve npm scopes when fetching package metadata |
| closed | aounkazmi-dev/Car-Show-Speed | [#2](https://github.com/aounkazmi-dev/Car-Show-Speed/pull/2) removing redirectives |
| closed | google-deepmind/concordia | [#383](https://github.com/google-deepmind/concordia/pull/383) Stop EntityAgent reusing stale pre-act values after a failed step |
| closed | google-deepmind/torax | [#2637](https://github.com/google-deepmind/torax/pull/2637) Normalize TGLF ExB rotation to the poloidal field |
| closed | mahmoud/boltons | [#470](https://github.com/mahmoud/boltons/pull/470) Reject BarrelList item indexes past the end |
| closed | ShaiqRaza/portfolioWebsiteFrontend | [#1](https://github.com/ShaiqRaza/portfolioWebsiteFrontend/pull/1) Media Query issue &amp;&amp; unneccesary imports  |

</details>

<details>
<summary><b>Pull requests in my own repositories</b> (19)</summary>

| Status | Repository | Pull request |
| :--- | :--- | :--- |
| merged | codewithfourtix/Car-Show-Speed | [#2](https://github.com/codewithfourtix/Car-Show-Speed/pull/2) Tested final version &amp;&amp; Updating fileName |
| merged | codewithfourtix/Car-Show-Speed | [#1](https://github.com/codewithfourtix/Car-Show-Speed/pull/1) removing directives |
| merged | codewithfourtix/descon-design | [#1](https://github.com/codewithfourtix/descon-design/pull/1) Changes |
| merged | codewithfourtix/ember | [#5](https://github.com/codewithfourtix/ember/pull/5) CI, tokenizer fix, and the --bench throughput harness |
| merged | codewithfourtix/ember | [#4](https://github.com/codewithfourtix/ember/pull/4) Phase 3: chat mode + kernel unit tests |
| merged | codewithfourtix/ember | [#3](https://github.com/codewithfourtix/ember/pull/3) Phase 2: INT8 / group-wise INT4 quantization |
| merged | codewithfourtix/ember | [#2](https://github.com/codewithfourtix/ember/pull/2) Phase 1: a working f32 forward pass (generates coherent text) |
| merged | codewithfourtix/ember | [#1](https://github.com/codewithfourtix/ember/pull/1) Project scaffold: modules, CLI, and correctness harness |
| merged | codewithfourtix/lofotixtest | [#2](https://github.com/codewithfourtix/lofotixtest/pull/2) FTUR: Email added automatically to view lost and found to enhance cre… |
| merged | codewithfourtix/lofotixtest | [#1](https://github.com/codewithfourtix/lofotixtest/pull/1) FTUR: Logic feature merge |
| merged | codewithfourtix/sachbatao | [#9](https://github.com/codewithfourtix/sachbatao/pull/9) feat(feedback): durably persist feedback labels |
| merged | codewithfourtix/sachbatao | [#8](https://github.com/codewithfourtix/sachbatao/pull/8) Feat/guardrails |
| merged | codewithfourtix/sachbatao | [#7](https://github.com/codewithfourtix/sachbatao/pull/7) fix(whatsapp): clear stale Chromium locks on startup |
| merged | codewithfourtix/sachbatao | [#5](https://github.com/codewithfourtix/sachbatao/pull/5) feat: per-sender rate limiting to cap API cost |
| merged | codewithfourtix/sachbatao | [#4](https://github.com/codewithfourtix/sachbatao/pull/4) fix(detector): always return a verdict for image/PDF content |
| merged | codewithfourtix/sachbatao | [#3](https://github.com/codewithfourtix/sachbatao/pull/3) fix(deploy): bump Docker image to Node 20 for pdf-parse |
| merged | codewithfourtix/sachbatao | [#2](https://github.com/codewithfourtix/sachbatao/pull/2) Add image (OCR) and PDF fraud checking |
| merged | codewithfourtix/sachbatao | [#1](https://github.com/codewithfourtix/sachbatao/pull/1) Feature/google cloud tts |
| open | codewithfourtix/lofotixtest | [#3](https://github.com/codewithfourtix/lofotixtest/pull/3) Manage items |

</details>

<sub>Rebuilt daily from the GitHub API by <a href="upstream.py">upstream.py</a>. Merges GitHub does not record, such as Copybara imports, are listed in <a href="upstream.json">upstream.json</a>.</sub>
<!-- upstream:end -->
