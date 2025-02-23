compile:
	rm -rf ./build && \
	rm -rf ./dist && \
	pyinstaller --onefile --noconsole main.py --name=Rollover_v1 --icon=s_a_logo.ico && \
	cp -r ./docs/* ./dist/ && \
	mkdir -p ./dist/demo && \
	cp -r ./demo/* ./dist/demo/ && \
	cd dist && \
	zip -r ../publish/rollover.zip ./*

deploy:
	aws s3 cp ./publish/rollover.zip s3://gelukkige-broodblik/Rollover/
	aws s3 cp ./dist/*.exe s3://gelukkige-broodblik/Rollover/releases/

markdown:
	python markdown.py