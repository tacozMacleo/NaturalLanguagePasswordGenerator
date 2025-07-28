 Natural Language Password Generator
===============================================================================

Ready to use Natural Language Password Generator.
Based on the idea that a adj. noun pair is easier to remember then a random
generated password, but still harder to brute-force.

Database source:
https://github.com/NaturalLanguagePasswords/system


Python versions supported: 3.7+

CLI Use case:
-------------------------------------------------------------------------------
`nlp`

For getting help menu:
`nlp --help`

For use in a script:
`nlp -s`


Package:
-------------------------------------------------------------------------------
Can also be used as a library.
```python
import nlp

password = nlp.get_password(pair_len=6)
```
run:
```python
help(nlp.get_password)
```
for more information on the function.

TODO:
===============================================================================
 * [ ] Add better support for script mode and multiple passwords.
