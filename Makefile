SOURCES := $(shell find . -type f -name '*.blend')

all: gltf
	
dae: $(patsubst ./%.blend, ./build/%.dae, ${SOURCES})
fbx: $(patsubst ./%.blend, ./build/%.fbx, ${SOURCES})
gltf: $(patsubst ./%.blend, ./build/%.gltf, ${SOURCES})


tex := $(shell find . -wholename './*.png')  # neess to filter out textures in build 
copiedtex: $(patsubst ./%.png, ./build/%.png, ${tex})
normaltex: $(patsubst ./%.png, ./build/%.normal.png, ${tex})

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

generate-normal-textures: copiedtex normaltex
	@echo "Generating normal textures: $<"
	#@echo "generating for $<"

./build/%.normal.png : ./build/%.png
	@echo "making for $@ depends on $<\n"
	@gegl -i $< -o $@ -- normal-map

./build/%.png : %.png
	@echo "copy $< to $$(dirname $@) \n"
	@mkdir -p $$(dirname $@)
	@cp $< $$(dirname $@);



clean-generate:
	@rm ./generated/*
clean:
	@rm -rf ./build
