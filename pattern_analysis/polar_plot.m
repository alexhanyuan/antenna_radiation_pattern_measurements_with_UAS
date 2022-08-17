% close all;
clear variables; clc;

collect_to_plot = 7;

filename{1} = '220414\20220414_174639_freq_446000000_fs_10000000.bin'; % noise 1k samples
filename{2} = '220414\20220414_175538_freq_446000000_fs_10000000.bin'; % crap ton of noise
filename{3} = '220414\20220414_120545_freq_446000000_fs_10000000.bin'; % CW tone 1k samples
filename{4} = '220415_data\20220415_103614_freq_445000000_fs_10000000_monopole.bin'; % monopole
filename{5} = '220415_data\20220415_102318_freq_445000000_fs_10000000.bin'; % yagi lmao it crashed halfway through
filename{6} = '220415_data\20220415_102102_freq_445000000_fs_10000000.bin'; % yagi
filename{7} = '220605_data\20220604_232531_freq_445000000_fs_10000000_top_NMO.bin'; % roof NMO
filename{8} = '220605_data\20220604_233209_freq_445000000_fs_10000000_hood_NMO.bin'; % hood NMO

fft_title = {'FFT of noise collect (1000 sample buffers)';
            'FFT of noise collect (10000 sample buffers)';
            'FFT of CW tone (1000 sample buffers)';
            'FFT of Monopole Collect';
            'FFT of yagi crash';
            'FFT of Yagi Collect';
            'FFT of -'};
polar_title = {'Polar plot of noise collect';
            'Polar plot of noise collect';
            'Polar plot of CW tone';
            'Colinear Monopole Radiation Pattern';
            'Yagi Crash Radiation Pattern';
            '5 Element Yagi Radiation Pattern';
            '1/4 Wave Roof Magnet NMO Mount Radiation Pattern';
            '1/4 Wave Hood Lip NMO Mount Radiation Pattern'};

show_stats = 1; % display signal stats
rolling_averages = 50; % window size of rolling average for polar plot

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

% figure(1) % plot collects showing peak power
% % set(gcf,'Position',[100 100 1400 600])
% % subplot(1,2,1)
% hold on, grid on
% ylabel('Relative Power (dB)')
% xlabel('FFT Bin')
% title(fft_title{collect_to_plot})
% % subtitle(fft_title{collect_to_plot})
% ylim([-130 -20])
% xlim([1 (fft_window*2)+1])

for ii = 1:num_buffers
    buffers(ii,:) = raw_data((((ii+1)*num_points)+1):(num_points*(ii+2)))';
    
    % extract peak power, can specify a window around fft_points/2 if cluttered
    max_power(ii) = max(buffers(ii,(num_points/2)-fft_window:(num_points/2)+fft_window));
%     plot(buffers(ii,(num_points/2)-fft_window:(num_points/2)+fft_window) + dbm_cal_offset)
end

M = movmean(max_power,rolling_averages); % moving mean
M = M - max(M); % normalize
% M = M - 50.1835;

azimuth = linspace(0,360,num_buffers)'; % generate azimuthal position vector

figure(1) % (2)
polarplot(azimuth*pi/180,M) % max_power)
title(polar_title{collect_to_plot})
rlim([-25 0])

if show_stats
    range = range(M)
    std_dev = std(M)
    variance = var(M)
end

% ax = gca;
% exportgraphics(ax,'220415_monopole.png','Resolution',600)
% exportgraphics(ax,'220415_yagi.png','Resolution',600)
% exportgraphics(ax,'220605_hood_vs_roof_mount_comparison.png','Resolution',600)