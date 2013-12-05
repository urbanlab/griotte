NOSETESTS := nosetests

# tests:
# 	@for i in `ls test/test_*.py`; do \
# 		echo "$$i =>" ; \
# 		PYTHONPATH=".:lib" python $$i ; \
# 		echo ; \
# 	done

tests:
	$(NOSETESTS) -d -v -P

cov:
	$(NOSETESTS) -d -v -P --with-coverage --cover-package=raspeomix

clean:
	@echo "Cleaning up byte compiled python stuff"
	find . -type f -regex ".*\.py[co]$$" -delete
	@echo "Cleaning up editor backup files"
	find . -type f \( -name "*~" -or -name "#*" \) -delete
	find . -type f \( -name "*.swp" \) -delete

