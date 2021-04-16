# levelsculpt

A level-creation program for platformers. Exports JSON.

There is no user manual yet. This is just for editors. I might break it up into multiple files but for now this is just in one big heap. There's no contents section yet, just get a markdown reader with a navigation overview.

## Project filesystem

All of the code (and the images) except for the driver (`main.py`) is stored in `/levelsculpt/levelsculpt/`.

#### Files and folders inside of /levelsculpt/levelsculpt/

- `assets/` contains images sounds etc.
- `common/` contains utility code that is not special to this projet and can be reused easily
- `storage/` contains code relating to the storage of the levels - both in memory and saving to disk.
- `ui/` contains code that interacts directly with the screen.
- `config.py` contains stuff like version, production name, defaults.

## Code hierarchy

`main.py` is the driver, but all it does is create a new `Application`.

#### Application class

The Application class `/levelsculpt/levelsculpt/ui/application.py` is the top level for organisation. It doesn't actually do much itself, though. All it does is create some panels for editing and create a window.

#### WorldViewport class

The WorldViewport class `/levelsculpt/levelsculpt/ui/worldviewport.py` doesn't do anything yet, and I think it's a bad idea to write documentation for something that you haven't even decided to organise yet.