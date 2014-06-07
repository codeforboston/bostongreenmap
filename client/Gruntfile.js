module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        handlebars: {
            options: {
                'amd': true
            },
            compile: {
                src: ['templates/**/*.hbs'],
                dest: "js/templates.js"
            }
        },
        compass: {
            dev: {
                options: {
                    sassDir: 'scss',
                    cssDir: 'build/css',
                    outputStyle: 'compressed'
                }
            },
            dist: {
                options: {
                    sassDir: 'scss',
                    cssDir: '<% project.buildPath %>',
                    outputStyle: 'compressed'
                }
            }
        },
        watch: {
            options: {
                livereload: {
                    port: 9002,
                    files: ['./**/*']
                }
            },
            handlebars: {
                files: ['templates/**/*'],
                tasks: ['default']
            },
            sass: {
                files: ['scss/**/*'],
                tasks: ['compass:dev']
            },
            js: {
                files: ['js/**/*.js'],
                tasks: []
            }
        },
        connect: {
            server: {
                options: {
                    hostname: '127.0.0.1',
                    port: 9008,
                    base: '.',
                    rules: {
                        '^(.*[^/])$': '$1.html',
                        '^(.*)/$': '$1/base.html'
                    }
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-handlebars');
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-connect');

    grunt.registerTask('default', [
        'handlebars:compile'
    ]);

    grunt.registerTask('dev', ['connect', 'watch']);
};
