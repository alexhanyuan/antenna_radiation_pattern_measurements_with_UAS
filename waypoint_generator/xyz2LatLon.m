function [Lat, Lon] = xyz2LatLon(origin_Lat, origin_Lon, origin_x, origin_y, x, y)

% Convert the distances between several xyz locations to Lat/Lon distances
% relative to the first location

%% if only x and y input arguments, relative to V1
if nargin == 2
    x = origin_Lat;
    y = origin_Lon;
    origin_x = 0;
    origin_y = 0;
    origin_Lat = 40.70925;
    origin_Lon = -77.9689;
end

%% Radius of the Earth in meters
RE = 6371000;

%% Convert degrees to distances
dx = (pi/180)*RE*cosd(mean(origin_Lat));
dy = (pi/180)*RE;

%% AUT origin in absolute meters
abs_origin_x_m = origin_x + (origin_Lon * dx);
abs_origin_y_m = origin_y + (origin_Lat * dy);

%% Relative abs
abs_x_m = abs_origin_x_m + x;
abs_y_m = abs_origin_y_m + y;

%% Reference meters to GPS coordinates
Lon = abs_x_m / dx;
Lat = abs_y_m / dy;

end