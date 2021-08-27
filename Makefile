SOURCES := $(wildcard ./**/*.blend)

all: gltf
	
dae: $(patsubst ./%.blend, ./build/%.dae, ${SOURCES})
fbx: $(patsubst ./%.blend, ./build/%.fbx, ${SOURCES})
gltf: $(patsubst ./%.blend, ./build/%.gltf, ${SOURCES})

./build/%.fbx: %.blend
	@echo "Build $@ from $<"
	@blender $< --background --python ./export-model.py -- $@ fbx > /dev/null

./build/%.dae: %.blend
	@echo "Build $@ from $<"
	@blender $< --background --python ./export-model.py -- $@ dae > /dev/null

./build/%.gltf: %.blend
	@echo "Build $@ from $<"
	@blender $< --background --python ./export-model.py -- $@ gltf > /dev/null

clean:
	@rm -rf ./build
