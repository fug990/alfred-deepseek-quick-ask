# Release checklist

1. Update the version in `info.plist`, `README.md`, and `CHANGELOG.md`.
2. Run `python3 -m unittest discover -s tests -v` and `plutil -lint info.plist`.
3. Export or package `DeepSeek-Quick-Ask-vX.Y.Z.alfredworkflow`.
4. Inspect the archive: `unzip -p outputs/DeepSeek-Quick-Ask-vX.Y.Z.alfredworkflow info.plist | plutil -extract variables xml1 -o - -`.
5. Confirm `DEEPSEEK_API_KEY` is empty and remains listed in `variablesdontexport`.
6. Create a GitHub release named `vX.Y.Z`, upload the workflow archive, and copy the matching section from `CHANGELOG.md` into the release notes.
