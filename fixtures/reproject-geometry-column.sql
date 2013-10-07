SELECT AddGeometryColumn('parks_park','geometry_26986',26986, 'MULTIPOLYGON', 2);
UPDATE parks_park SET geometry_26986 = ST_Transform(geometry,26986);
SELECT UpdateGeometrySRID('parks_park','geometry',26986);
UPDATE parks_park SET geometry = geometry_26986;
ALTER TABLE parks_park DROP COLUMN geometry_26986;