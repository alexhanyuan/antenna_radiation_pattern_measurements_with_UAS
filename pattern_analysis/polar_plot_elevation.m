close all; 
clear variables; clc;

collect_to_plot = 2;

filename{1} = '220611_data\20220604_235522_freq_243700000_fs_10000000_terele3.bin'; % terele dish
% filename{1} = '220611_data\20220604_234206_freq_243700000_fs_10000000_terele4.bin'; % terele dish
filename{2} = '220611_data\20220604_234525_freq_146520000_fs_10000000_58_lastone.bin'; % 5/8 wave whip
filename{3} = '220611_data\20220604_233842_freq_146520000_fs_10000000_14wave_last_one.bin'; % 1/4 wave whip

fft_title = {'FFT of Parabolic Dish';
            'FFT of VHF 5/8ths Wave NMO Whip';
            'FFT of VHF 1/4 Wave NMO Whip'};
polar_title = {'Parabolic Dish Elevation Radiation Pattern Cut';
            'VHF 5/8ths Wave NMO Whip Elevation Radiation Pattern Cut';
            'VHF 1/4 Wave NMO Whip Elevation Radiation Pattern Cut'};

plot_ffts = 0; % plot ffts
show_stats = 0; % display signal stats
rolling_averages = 70; % window size of rolling average for polar plot

dbm_cal_offset = -102; % difference in HackRF measured dB and actual dBm

f = fopen(filename{collect_to_plot}, 'rb');
raw_data = fread(f, Inf, 'float')'; % read in data
fclose('all');

num_points = 512; % number of extracted fft points in GRC flowgraph
num_buffers = (length(raw_data)/num_points)-2; % also azimuths
fft_window = 20; % pick out AUT signal

% array and cell initializations
buffers = zeros(num_buffers,num_points);
max_power = zeros(num_buffers,1);

if plot_ffts
    figure % plot collects showing peak power
    % set(gcf,'Position',[100 100 1400 600])
    % subplot(1,2,1)
    hold on, grid on
    ylabel('Relative Power (dB)')
    xlabel('FFT Bin')
    title(fft_title{collect_to_plot})
    % subtitle(fft_title{collect_to_plot})
    ylim([-130 -20])
    xlim([1 (fft_window*2)+1])
end

for ii = 1:num_buffers
    buffers(ii,:) = raw_data((((ii+1)*num_points)+1):(num_points*(ii+2)))';
    
    % extract peak power, can specify a window around fft_points/2 if cluttered
    max_power(ii) = max(buffers(ii,(num_points/2)-fft_window:(num_points/2)+fft_window));
    if plot_ffts
        plot(buffers(ii,(num_points/2)-fft_window:(num_points/2)+fft_window) + dbm_cal_offset)
    end
end

% max_power = max_power - max(max_power); % normalize
M = movmean(max_power,rolling_averages); % moving mean
M = M - max(M); % normalize
% M = M - 56.1339;

elevation = linspace(90,180,num_buffers)'; % generate elevation position vector
mirrored_elevation = linspace(90,0,num_buffers)'; % generate mirrored elevation position vector


if collect_to_plot == 1
    elevation_data = [flipud(M(171:end)); M(171:end)];
    elevation_vector = linspace(180,0,length(M(171:end))*2)';
    
%     elevation_data = [flipud(M(1:4184)); M(1:4184)];
%     elevation_vector = linspace(180,0,4184*2)';
end

if collect_to_plot == 2
    elevation_data = [flipud(M(215:3711)); M(215:3711)];
    elevation_vector = linspace(180,0,3497*2)';
end

% elevation_data = [flipud(M(1:4034)); M(1:4034)];
% elevation_vector = linspace(180,0,4034*2)';

if collect_to_plot == 3
    elevation_data = [flipud(M); M];
    elevation_vector = linspace(180,0,num_buffers*2)';
end

figure
plot(M)
title('Peak Power Linear Plot')

figure(3)
% hold on
% subplot(1,2,2)
polarplot(elevation_vector*pi/180,elevation_data) % max_power)
title(polar_title{collect_to_plot})
thetalim([0 180])

% subtitle(polar_title{collect_to_plot})
rlim([-30 0])
% rticks(-30:10:70)
% rticklabels({'r = -2','r = 3','r = 9','r = 15'})

if show_stats
    range = range(M)
    std_dev = std(M)
    variance = var(M)
end

% ax = gca;
% exportgraphics(ax,'220611_terele_dish.png','Resolution',600)
% exportgraphics(ax,'220611_58ths_wave_whip.png','Resolution',600)