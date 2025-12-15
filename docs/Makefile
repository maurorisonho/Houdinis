# Makefile for Sphinx documentation

# You can set these variables from the command line
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help"
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Install documentation dependencies
install:
	pip install -r requirements.txt

# Build HTML documentation
html:
	@echo "Building HTML documentation..."
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)
	@echo
	@echo "Build finished. Open _build/html/index.html in your browser."

# Clean build directory
clean:
	@echo "Cleaning build directory..."
	@rm -rf $(BUILDDIR)/*
	@echo "Clean complete."

# Serve documentation locally
serve:
	@echo "Serving documentation at http://localhost:8000"
	@echo "Press Ctrl+C to stop the server"
	@cd $(BUILDDIR)/html && python -m http.server 8000

# Build and serve
livehtml: html serve

# Check for broken links
linkcheck:
	@$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS)

# Build PDF documentation (requires LaTeX)
pdf:
	@$(SPHINXBUILD) -b latex "$(SOURCEDIR)" "$(BUILDDIR)/latex" $(SPHINXOPTS)
	@cd $(BUILDDIR)/latex && make

# Catch-all target: route all unknown targets to Sphinx
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
