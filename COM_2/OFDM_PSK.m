close all;
clear all;
clc;

% https://www.mathworks.com/help/comm/ug/fading-channels.html

%%
M = 2; % M-PSK
Nofdm = 64;     % numero de subportadoras OFDM
Ncp = 16;       % tamanho do prefixo ciclico

EbN0dB = -8:4:36; % bit to noise ratio

nIteracoes = 2^10; 
BER = zeros(1,length(EbN0dB));
BER_M = zeros(1,length(EbN0dB));

BERcoded = zeros(1,length(EbN0dB));
BER_Mcoded = zeros(1,length(EbN0dB));

%% TX
message = randi([0 M-1],Nofdm/2,log2(M)); % colocar zeros de cauda
mensagem = randi([0 M-1],Nofdm,log2(M));

trelica = poly2trellis(7,[133 171]);
msgcoded = convenc(message,trelica);
tbdepth = 2;
msgviterbi = vitdec(msgcoded,trelica,tbdepth,'trunc','hard');
indBER = find(message ~= msgviterbi)
BER
% M-PSK Modulation
DataPSKcoded = pskmod(msgcoded,M);
TX = ifft(DataPSKcoded);
TXofdmcoded = [TX(Nofdm-Ncp+1:Nofdm); TX];

% M-PSK Modulation
DataPSK = pskmod(mensagem,M);
% teste BPSK com canal awgn
DataPSKawgn = awgn(DataPSK,10);
scatterplot(DataPSKawgn)

TX = ifft(DataPSK);
TXofdm = [TX(Nofdm-Ncp+1:Nofdm); TX];

for ni = 1:length(EbN0dB)
    for nInter = 1:nIteracoes

%% Canal
        Yofdm = awgn(TXofdmcoded,EbN0dB(1,ni));

%% Receptor
        RXofdm = Yofdm(Ncp+1:end);
        RX = fft(RXofdm);
        % demodulador
        msg = pskdemod(RX,M);
        % decodificador
        msgviterbi = vitdec(msg,trelica,tbdepth,'trunc','hard');
        indBER = find(message ~= msgviterbi);

        Ber_M = length(indBER);
        BER_Mcoded(1,ni) = BER_Mcoded(1,ni) + Ber_M;

%% canal        
        Yofdm = awgn(TXofdm,EbN0dB(1,ni));

%% Receptor
        RXofdm = Yofdm(Ncp+1:end);
        RX = fft(RXofdm);
        % demodulador
        msg = pskdemod(RX,M);
        indBER = find(mensagem ~= msg);

        Ber_M = length(indBER);
        BER_M(1,ni) = BER_M(1,ni) + Ber_M;       
    end
    BER(1,ni) = BER_M(1,ni)/(log2(M)*nIteracoes*Nofdm)
    BERcoded(1,ni) = BER_M(1,ni)/(log2(M)*nIteracoes*Nofdm/2) 
end

close all; 
figure
semilogy(EbN0dB,BER,'bx-','LineWidth',2);
hold on
semilogy(EbN0dB,BERcoded,'go-','LineWidth',2);
grid on
xlabel('Eb/No, dB')
ylabel('Bit Error Rate')
title('BER for M-PSK')

