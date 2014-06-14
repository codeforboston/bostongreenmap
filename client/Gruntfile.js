module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        handlebars: {
            options: {
                'amd': true
            },
            compile: {
                src: ['templates/*'],
                dest: "build/templates.js"
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
                    cssDir: 'build',
                    outputStyle: 'compressed'
                }
            }
        },
        watch: {
            handlebars: {
                files: ['templates/**/*'],
                tasks: ['handlebars:compile']
            },
            sass: {
                files: ['scss/*'],
                tasks: ['compass:dev']
            },
            js: {
                files: ['js/**/*.js'],
                tasks: ['compass:dev']
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

    grunt.registerTask('server', ['connect', 'watch']);
    grunt.registerTask('default', []);

};
