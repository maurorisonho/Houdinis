#  Translation Guidelines for Houdinis

This document provides guidelines for translating Houdinis documentation into multiple languages.

##  Available Languages

| Language | Code | Status | README | Maintainer |
|----------|------|--------|--------|------------|
| English | `en` |  Complete | [README.md](../../README.md) | @maurorisonho |
| Portuguese (Brasil) | `pt-BR` |  Complete | [README.pt-BR.md](../../README.pt-BR.md) | @maurorisonho |
| Español | `es` |  Complete | [README.es.md](../../README.es.md) | @maurorisonho |
|  () | `zh` |  Complete | [README.zh.md](../../README.zh.md) | @maurorisonho |
| Français | `fr` |  Planned | - | - |
| Deutsch | `de` |  Planned | - | - |
|  | `ja` |  Planned | - | - |
| Русский | `ru` |  Planned | - | - |

---

##  Translation Principles

### 1. **Accuracy First**
- Maintain technical accuracy above all
- Preserve code examples exactly (only translate comments)
- Keep mathematical notation unchanged
- Maintain links and references

### 2. **Cultural Adaptation**
- Use culturally appropriate examples
- Adapt idioms and metaphors
- Use local date/time formats
- Consider regional terminology preferences

### 3. **Consistency**
- Use consistent terminology throughout
- Maintain glossary of technical terms
- Follow language-specific style guides
- Keep formatting consistent with English version

### 4. **Completeness**
- Translate all sections, not just summaries
- Include all code examples with translated comments
- Translate image alt text and captions
- Update all links to translated versions when available

---

##  Translation Workflow

### Step 1: Preparation

1. **Read English Version**: Fully understand the content
2. **Check Glossary**: Review technical terms in [glossary](#-technical-glossary)
3. **Setup Environment**: Create branch `i18n/<language-code>`

### Step 2: Translation

1. **Create File**: `README.<language-code>.md`
2. **Header Section**: Translate title, badges, quote
3. **Main Content**: Translate all sections sequentially
4. **Code Comments**: Translate comments in code examples
5. **Links**: Update links to translated versions

### Step 3: Review

1. **Technical Review**: Verify accuracy of technical terms
2. **Language Review**: Check grammar and style
3. **Formatting Review**: Ensure markdown renders correctly
4. **Link Verification**: Test all internal and external links

### Step 4: Submission

1. **Self-Review**: Complete checklist below
2. **Create PR**: Submit pull request with description
3. **Address Feedback**: Respond to review comments
4. **Update Glossary**: Add new terms to glossary

---

##  Translation Checklist

Use this checklist for each translation:

### Content Completeness
- [ ] Title and project description
- [ ] Features section
- [ ] Installation instructions
- [ ] Quick start guide
- [ ] Architecture documentation
- [ ] Algorithm descriptions
- [ ] Usage examples (with translated comments)
- [ ] PQC section
- [ ] Backend documentation
- [ ] Testing instructions
- [ ] Docker/Kubernetes guides
- [ ] Contributing guidelines
- [ ] License information
- [ ] Contact information

### Technical Accuracy
- [ ] All code examples unchanged (except comments)
- [ ] Command-line examples unchanged
- [ ] File paths unchanged
- [ ] URLs and links working
- [ ] Mathematical notation preserved
- [ ] Algorithm names consistent

### Formatting
- [ ] Markdown renders correctly
- [ ] Tables formatted properly
- [ ] Code blocks have correct syntax highlighting
- [ ] Emojis display correctly
- [ ] Badges work correctly
- [ ] Lists and hierarchies correct

### Language Quality
- [ ] Grammar checked
- [ ] Spelling verified
- [ ] Technical terms consistent
- [ ] Style appropriate for audience
- [ ] No machine translation artifacts
- [ ] Natural flow and readability

---

##  Technical Glossary

Maintain consistent translations for these terms:

### Core Concepts

| English | PT-BR | ES | ZH | Notes |
|---------|-------|----|----|-------|
| Quantum Cryptanalysis | Criptoanálise Quântica | Criptoanálisis Cuántico |  | - |
| Quantum Algorithm | Algoritmo Quântico | Algoritmo Cuántico |  | - |
| Quantum Computer | Computador Quântico | Computadora Cuántica |  | - |
| Quantum Circuit | Circuito Quântico | Circuito Cuántico |  | - |
| Qubit | Qubit | Qubit |  | Keep English term |
| Quantum Gate | Porta Quântica | Puerta Cuántica |  | - |
| Quantum Backend | Backend Quântico | Backend Cuántico |  | - |
| Quantum Simulator | Simulador Quântico | Simulador Cuántico |  | - |

### Algorithms

| English | PT-BR | ES | ZH | Notes |
|---------|-------|----|----|-------|
| Shor's Algorithm | Algoritmo de Shor | Algoritmo de Shor | Shor  | - |
| Grover's Algorithm | Algoritmo de Grover | Algoritmo de Grover | Grover  | - |
| Simon's Algorithm | Algoritmo de Simon | Algoritmo de Simon | Simon  | - |
| Quantum Phase Estimation | Estimação de Fase Quântica | Estimación de Fase Cuántica |  | - |
| Amplitude Amplification | Amplificação de Amplitude | Amplificación de Amplitud |  | - |
| Deutsch-Jozsa | Deutsch-Jozsa | Deutsch-Jozsa | Deutsch-Jozsa | Keep name |
| Bernstein-Vazirani | Bernstein-Vazirani | Bernstein-Vazirani | Bernstein-Vazirani | Keep name |

### Cryptography

| English | PT-BR | ES | ZH | Notes |
|---------|-------|----|----|-------|
| Public Key Cryptography | Criptografia de Chave Pública | Criptografía de Clave Pública |  | - |
| Symmetric Cryptography | Criptografia Simétrica | Criptografía Simétrica |  | - |
| Post-Quantum Cryptography | Criptografia Pós-Quântica | Criptografía Post-Cuántica |  | - |
| Key Exchange | Troca de Chaves | Intercambio de Claves |  | - |
| Digital Signature | Assinatura Digital | Firma Digital |  | - |
| Hash Function | Função Hash | Función Hash |  | - |
| Encryption | Criptografia / Cifração | Cifrado |  | Context dependent |
| Decryption | Descriptografia / Decifração | Descifrado |  | - |

### Security

| English | PT-BR | ES | ZH | Notes |
|---------|-------|----|----|-------|
| Vulnerability | Vulnerabilidade | Vulnerabilidad |  | - |
| Exploit | Exploit / Exploração | Exploit / Explotación |  | - |
| Attack | Ataque | Ataque |  | - |
| Side-Channel Attack | Ataque de Canal Lateral | Ataque de Canal Lateral |  | - |
| Timing Attack | Ataque de Temporização | Ataque de Tiempo |  | - |
| Penetration Testing | Teste de Penetração | Pruebas de Penetración |  | - |
| Security Audit | Auditoria de Segurança | Auditoría de Seguridad |  | - |

### Infrastructure

| English | PT-BR | ES | ZH | Notes |
|---------|-------|----|----|-------|
| Backend | Backend | Backend |  | Keep English in code |
| Framework | Framework | Framework |  | - |
| Module | Módulo | Módulo |  | - |
| Library | Biblioteca | Biblioteca |  | - |
| API | API | API | API | Keep English |
| Deployment | Implantação | Despliegue |  | - |
| Container | Container | Contenedor |  | - |
| Orchestration | Orquestração | Orquestación |  | - |

---

##  Style Guidelines

### Portuguese (PT-BR)

**Formality**: Use formal "você" (not "tu")
**Tone**: Professional but approachable
**Code Terms**: Keep English terms in code contexts
**Examples**:
-  "Execute o comando `python main.py`"
-  "Execute o comando `pitão main.py`"

### Spanish (ES)

**Dialect**: Use neutral Spanish (avoid regionalisms)
**Formality**: Use formal "usted" for documentation
**Tone**: Professional and clear
**Code Terms**: Keep English terms in code contexts
**Examples**:
-  "Ejecute el comando `python main.py`"
-  "Ejecutá el comando `python main.py`" (avoid voseo)

### Chinese (ZH)

**Variant**: Use Simplified Chinese ()
**Formality**: Professional and direct
**Tone**: Clear and concise
**Code Terms**: Keep English terms in code contexts
**Punctuation**: Use Chinese punctuation ()
**Examples**:
-  " `python main.py`"
-  " ` main.py`"

---

##  Translation Tools

### Recommended Tools

1. **CAT Tools**:
   - [OmegaT](https://omegat.org/) - Free CAT tool
   - [Poedit](https://poedit.net/) - For i18n files
   - [Crowdin](https://crowdin.com/) - Collaborative translation

2. **Quality Assurance**:
   - [LanguageTool](https://languagetool.org/) - Grammar checking
   - [Grammarly](https://www.grammarly.com/) - English review
   - [DeepL](https://www.deepl.com/) - Translation reference (NOT for direct copy)

3. **Technical Glossaries**:
   - [Microsoft Terminology](https://www.microsoft.com/en-us/language)
   - [IBM Terminology](https://www.ibm.com/docs/en/terminology)
   - [ISO Standards](https://www.iso.org/)

### Markdown Validation

```bash
# Check markdown syntax
npx markdownlint-cli README.*.md

# Check links
npx markdown-link-check README.*.md

# Preview rendering
grip README.<lang>.md
```

---

##  Automation

### Translation Memory

Maintain translation memory in `docs/i18n/translation-memory/`:

```
docs/i18n/translation-memory/
 en-pt-BR.tmx
 en-es.tmx
 en-zh.tmx
 glossary.json
```

### CI/CD Checks

Automated checks in CI pipeline:

- [ ] Markdown syntax validation
- [ ] Link checking
- [ ] Glossary consistency
- [ ] Code block preservation
- [ ] Translation completeness

---

##  Getting Help

### Translation Questions

- **Technical Terms**: Check glossary first, then ask in issue
- **Context Unclear**: Reference English version, ask maintainer
- **Style Questions**: Refer to style guide, check existing translations

### Community

- **Discord**: [Join our server](https://discord.gg/houdinis) (coming soon)
- **GitHub Discussions**: [Discuss translations](https://github.com/maurorisonho/Houdinis/discussions)
- **Email**: maurorisonho@gmail.com

---

##  Translation Credits

### Contributors

| Language | Translator(s) | Date | Version |
|----------|---------------|------|---------|
| PT-BR | @maurorisonho | 2025-01 | 1.0 |
| ES | @maurorisonho | 2025-01 | 1.0 |
| ZH | @maurorisonho | 2025-01 | 1.0 |

Want to see your name here? [Contribute a translation!](../../CONTRIBUTING.md)

---

##  License

Translations are subject to the same [MIT License](../../LICENSE) as the main project.

---

**Thank you for helping make Houdinis accessible to the world! **
