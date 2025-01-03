blender :=/snap/bin/blender  # distro specific, probably should just assume blender is on path for this script
############################3

SOURCES := $(shell find . -type f -name '*.blend')

all: gltf textures
	
dae: $(patsubst ./%.blend, ./build/%.dae, ${SOURCES})
fbx: $(patsubst ./%.blend, ./build/%.fbx, ${SOURCES})
gltf: $(patsubst ./%.blend, ./build/%.gltf, ${SOURCES})


tex_png := $(shell find . -wholename './*.png' | grep -v build) 
copiedtex_png: $(patsubst ./%.png, ./build/%.png, ${tex_png})
normaltex_png: $(patsubst ./%.png, ./build/%.normal.png, ${tex_png})

tex_jpg := $(shell find . -wholename './*.jpg' | grep -v build)  
copiedtex_jpg: $(patsubst ./%.jpg, ./build/%.jpg, ${tex_jpg})
normaltex_jpg: $(patsubst ./%.jpg, ./build/%.normal.jpg, ${tex_jpg})

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

textures: copiedtex_png normaltex_png copiedtex_jpg normaltex_jpg


./build/%.normal.png : ./build/%.png
	@echo "making for $@ depends on $<\n"
	@gegl -i $< -o $@ -- normal-map

./build/%.png : %.png
	@echo "copy $< to $$(dirname $@) \n"
	@mkdir -p $$(dirname $@)
	@cp $< $$(dirname $@);

./build/%.normal.jpg : ./build/%.jpg
	@echo "making for $@ depends on $<\n"
	@gegl -i $< -o $@ -- normal-map

./build/%.jpg : %.jpg
	@echo "copy $< to $$(dirname $@) \n"
	@mkdir -p $$(dirname $@)
	@cp $< $$(dirname $@);


animation: 
	echo "build animations"
	@blender $< --python ./import-animations.py

clean-generate:
	@rm ./generated/*

clean:
	@rm -rf ./build
