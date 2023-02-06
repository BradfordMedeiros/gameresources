SOURCES := $(shell find . -type f -name '*.blend')

all: gltf
	
dae: $(patsubst ./%.blend, ./build/%.dae, ${SOURCES})
fbx: $(patsubst ./%.blend, ./build/%.fbx, ${SOURCES})
gltf: $(patsubst ./%.blend, ./build/%.gltf, ${SOURCES})

fixmodels: $(patsubst ./%.blend, %.blend.update, ${SOURCES})
validate:
	@./check-models.sh || true

./build/%.fbx: %.blend
	@echo "Build $@ from $<"
	@blender $< --background --python ./export-model.py -- $@ fbx > /dev/null

./build/%.dae: %.blend
	@echo "Build $@ from $<"
	@blender $< --background --python ./export-model.py -- $@ dae > /dev/null

./build/%.gltf: %.blend
	@echo "Build $@ from $<"
	@blender $< --background --python ./export-model.py -- $@ gltf > /dev/null

%.blend.update : %.blend
	@echo "Updating model $<"
	@blender $< --background --python ./try-fixmodel.py -- $@ > /dev/null

generate-models:
	@echo "Generating models"
	#blender $< --background --python ./generate-models.py -- $@ #> /dev/null
	@blender $< --python ./generate-models.py -- $@

clean-generate:
	@rm ./generated/*
clean:
	@rm -rf ./build
