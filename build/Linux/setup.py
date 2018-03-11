from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict (packages = []
                    ,includes = ['re']
                    ,excludes = []
                    )

executables = [Executable ('samurai.py'
                          ,base       = 'Console'
                          ,targetName = 'samurai'
                          )
              ]

setup (name        = 'samurai'
      ,version     = '1'
      ,description = 'A minimalistic text-only browser'
      ,options     = dict(build_exe=buildOptions)
      ,executables = executables
      )
