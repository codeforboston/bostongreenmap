/* Color Definitions */

@park: #00DC00;
@park_label: #777;

/* Font Definitions */

@font_regular: "Open Sans Regular";
@font_italic: "Open Sans Italic";
@font_medium: "Open Sans Bold";

/* Parks */

#park-labels {
  
  text-face-name: @font_italic;
  text-name: "[name]";
  text-fill: darken(@park, 20%);
  text-halo-fill: white;
  text-min-distance: 70;
  text-wrap-width: 50;
  text-character-spacing: 2;
    
  [zoom >= 12] { text-size: 9 }
  [zoom >= 13] { text-size: 10 }
  [zoom >= 14] {
    text-size: 12;
    text-character-spacing: 3;
  }
  [zoom >= 16] { text-size: 14 }

}

#park-geometry {
  
  line-color: darken(@park, 20%);
  line-width: 0.5;
  polygon-opacity:0.8;
  polygon-fill:@park;
  
}