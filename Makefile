SOURCES := $(wildcard ./**/*.blend)

all: fbx
	
dae: $(patsubst ./%.blend, ./build/%.dae, ${SOURCES})
fbx: $(patsubst ./%.blend, ./build/%.fbx, ${SOURCES})

./build/%.fbx: %.blend
	@echo "Build $@ from $<"
	@blender $< --background --python ./export-model.py -- $@ fbx > /dev/null

./build/%.dae: %.blend
	@echo "Build $@ from $<"
	@blender $< --background --python ./export-model.py -- $@ dae > /dev/null

clean:
	@rm -rf ./build
