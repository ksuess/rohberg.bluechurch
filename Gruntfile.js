module.exports = function (grunt) {
    'use strict';
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        // we could just concatenate everything, really
        // but we like to have it the complex way.
        // also, in this way we do not have to worry
        // about putting files in the correct order
        // (the dependency tree is walked by r.js)
        less: {
            dist: {
                options: {
                    paths: [],
                    strictMath: false,
                    sourceMap: true,
                    outputSourceFiles: true,
                    sourceMapFileInline: false,
                    sourceMapURL: '++theme++bluechurch/less/theme-compiled.less.map',
                    sourceMapFilename: 'less/theme-compiled.less.map',
                    modifyVars: {
                        "isPlone": "false"
                    }
                },
                files: {
                    'less/theme-compiled.css': 'less/theme.local.less',
                }
            }
        },
        postcss: {
            options: {
                map: true,
                processors: [
                    require('autoprefixer')({
                        browsers: ['last 2 versions']
                    })
                ]
            },
            dist: {
                src: 'less/*.css'
            }
        },
        shell: {
            greet: {
                command: greeting => 'say ' + greeting
            }
        },
        watch: {
            scripts: {
                files: [
                    'less/*.less',
                    'barceloneta/less/*.less'
                ],
                tasks: ['less', 'postcss', 'shell:greet:watch done']
            }
        },
        browserSync: {
            html: {
                bsFiles: {
                    src : [
                      'less/*.less',
                      'barceloneta/less/*.less',
                      '*.html'
                    ]
                },
                options: {
                    watchTask: true,
                    debugInfo: true,
                    online: true,
                    server: {
                        baseDir: "."
                    },
                }
            },
            plone: {
                bsFiles: {
                    src : [
                      'less/*.less',
                      'barceloneta/less/*.less',
                      '*.html',
                      '*.xml'
                    ]
                },
                options: {
                    watchTask: true,
                    // debugInfo: true,
                    proxy: "localhost:10680",
                    // reloadDelay: 10000,
                    // reloadDebounce: 2000,
                    online: false
                }
            }
        }
    });


    // grunt.loadTasks('tasks');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-postcss');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-browser-sync');
    grunt.loadNpmTasks('grunt-shell');

    // CWD to theme folder
    grunt.file.setBase('./src/rohberg/bluechurch/theme');

    grunt.registerTask('compile', ['less', 'postcss']);
    grunt.registerTask('default', ['compile']);
    grunt.registerTask('bsync', ["browserSync:html", "watch"]);
    grunt.registerTask('plone-bsync', ["browserSync:plone", "watch"]);
    // grunt.registerTask('plone-bsync', [ "watch", "browserSync:plone"]);
};
