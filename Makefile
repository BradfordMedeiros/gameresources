SOURCES := $(wildcard ./**/*.blend)
OBJ :=$(patsubst %.blend, %.fbx, ${SOURCES})

all: $(OBJ)

%.fbx: %.blend
	@blender $< --background --python ./export-model.py -- $@

clean:
	@rm -rf ./build
