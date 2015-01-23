module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        handlebars: {
            options: {
                'amd': true
            },
            compile: {
                src: ['client/templates/*'],
                dest: "client/build/templates.js"
            }
        },
        compass: {
            dev: {
                options: {
                    sassDir: 'client/scss',
                    cssDir: 'client/build/css',
                    outputStyle: 'compressed'
                }
            },
            dist: {
                options: {
                    sassDir: 'client/scss',
                    cssDir: 'client/build',
                    outputStyle: 'compressed'
                }
            }
        },
        watch: {
            handlebars: {
                files: ['client/templates/**/*'],
                tasks: ['handlebars:compile']
            },
            sass: {
                files: ['client/scss/**/*.scss'],
                tasks: ['compass:dev']
            },
            js: {
                files: ['client/js/**/*.js'],
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
