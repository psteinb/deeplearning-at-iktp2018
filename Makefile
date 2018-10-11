all: index.html

prepare :
	bundle config --local github.https true
	bundle --path=.bundle/gems --binstubs=.bundle/.bin
	git clone -b 3.6.0 --depth 1 https://github.com/hakimel/reveal.js.git || true


%.html : %.adoc
	bundle exec asciidoctor-revealjs $<
