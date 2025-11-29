% -------------------------------------------------------------
% Avaliação 4 – OFDM – COM29008
% Simulação de um sistema OFDM em banda base
% Canal AWGN, 64 subportadoras, CP = 16
% Modulações: 4-QAM, 16-QAM e 64-QAM
%
% Especificação (IEEE 802.11 simplificado):
% - 64 subportadoras OFDM
% - 16 amostras de prefixo cíclico
% - 4 subportadoras piloto
% - 1 componente DC (sempre zero)
% - 6 zeros PAD nas primeiras subportadoras
% - 5 zeros PAD nas últimas subportadoras
% -------------------------------------------------------------

clear all;
close all;
clc;

%% ----------------- PARÂMETROS DO SISTEMA --------------------

Nsub  = 64;            % número total de subportadoras OFDM
Ncp   = 16;            % tamanho do prefixo cíclico
SNRdB = -8:4:40;       % SNR em dB: -8, -4, 0, ..., 40
Niter = 1e4;           % número de iterações (símbolos OFDM) por ponto de SNR

% Conjunto de ordens de modulação QAM
Mvec = [4 16 64];      % 4-QAM (QPSK), 16-QAM, 64-QAM

% Vetor para acumular a BER
BER = zeros(length(SNRdB), length(Mvec));

%% ----------------- MAPEAMENTO DAS SUBPORTADORAS -------------

% Estrutura de 64 subportadoras (IEEE 802.11):
% - 6 subportadoras iniciais de PAD (zeros)
% - 48 subportadoras de dados
% - 4 subportadoras piloto
% - 1 subportadora DC (zero)
% - 5 subportadoras finais de PAD (zeros)

dataIndex  = [7:31 35:59];   % índices das 48 subportadoras de dados
pilotIndex = [32 34 60 61];  % índices das 4 subportadoras piloto
dcIndex    = 33;             % índice da subportadora DC (sempre zero)

Ndata = length(dataIndex);   % número de subportadoras de dados (48)

%% ----------------- LAÇO SOBRE MODULAÇÕES ---------------------

for m = 1:length(Mvec)
    
    M = Mvec(m);          % ordem da modulação atual
    k = log2(M);          % número de bits por símbolo QAM
    
    fprintf('\n--- Simulação para M = %d-QAM ---\n', M);
    
    %% -------------- LAÇO SOBRE VALORES DE SNR ----------------
    
    for s = 1:length(SNRdB)
        
        SNR = SNRdB(s);
        
        % Contadores de erros e bits transmitidos
        numErr  = 0;
        numBits = 0;
        
        %% ---------- LAÇO PRINCIPAL DE SIMULAÇÃO --------------
        % Cada iteração transmite 1 símbolo OFDM (48 símbolos QAM de dados)
        
        for it = 1:Niter
            
            % 1) Geração dos símbolos de informação (inteiros 0..M-1)
            %    Cada subportadora de dados carrega 1 símbolo QAM.
            dataSym_tx = randi([0 M-1], Ndata, 1);
            
            % 2) Modulação QAM em banda base -------------------
            %    qammod padrão (inteiro → símbolo complexo)
            %    (mapeamento Gray por padrão no MATLAB)
            symbols_tx = qammod(dataSym_tx, M);
                       
            % 3) Montagem do vetor de subportadoras ------------
            %    X: vetor de 64 amostras em frequência (domínio da FFT)
            X = zeros(Nsub, 1);
            
            %   - Insere símbolos de dados nas subportadoras de dados
            X(dataIndex) = symbols_tx;
            
            %   - Insere pilotos (valores conhecidos, por ex. +1)
            X(pilotIndex) = 1 + 0j;
            
            %   - Subportadora DC é forçada a zero
            X(dcIndex) = 0;
            
            %   - Demais subportadoras (PAD) já são zero
            %     por causa da inicialização X = 0.
            
            % 4) IFFT: converte para o domínio do tempo --------
            x = ifft(X, Nsub);   % símbolo OFDM em banda base (tempo discreto)
            
            % 5) Adiciona prefixo cíclico ----------------------
            x_cp = [x(end-Ncp+1:end); x];  % concatena CP + símbolo OFDM
            
            % 6) Canal AWGN ------------------------------------
            %    Ruído branco com SNR especificada em relação
            %    à potência medida do sinal transmitido.
            y_cp = awgn(x_cp, SNR, 'measured');
            
            % 7) Remoção do prefixo cíclico --------------------
            y = y_cp(Ncp+1:end);
            
            % 8) FFT: volta para o domínio da frequência -------
            Y = fft(y, Nsub);
            
            % 9) Equalização em frequência ---------------------
            %    Canal gaussiano ideal (h = 1), logo não é
            %    necessário dividir por H(f). Mantemos Y.
            Yeq = Y;
            
            % 10) Seleciona apenas as subportadoras de dados ---
            symbols_rx = Yeq(dataIndex);
            
            % 11) Demodulação QAM ------------------------------
            %     símbolos recebidos → inteiros 0..M-1
            dataSym_rx = qamdemod(symbols_rx, M);
            
            % 12) Conversão inteiro → bits (para BER de bits) ---
            %     Converte cada símbolo em k bits (linha por símbolo)
            bits_tx_mat = de2bi(dataSym_tx, k, 'left-msb');
            bits_rx_mat = de2bi(dataSym_rx, k, 'left-msb');
            
            % Empilha em vetores coluna
            bits_tx_vec = bits_tx_mat.';
            bits_rx_vec = bits_rx_mat.';
            bits_tx_vec = bits_tx_vec(:);
            bits_rx_vec = bits_rx_vec(:);
            
            % 13) Cálculo de erros de bit ----------------------
            numErr  = numErr  + sum(bits_rx_vec ~= bits_tx_vec);
            numBits = numBits + length(bits_tx_vec);
            
        end % for it
        
        % 14) Cálculo da BER para este ponto de SNR -----------
        BER(s, m) = numErr / numBits;
        
        fprintf('SNR = %3d dB -> BER = %.3e\n', SNR, BER(s, m));
        
    end % for s
    
end % for m

%% ------------------ GRÁFICO DA BER ---------------------------

figure;
semilogy(SNRdB, BER(:,1), 'bo-','LineWidth',2); hold on;
semilogy(SNRdB, BER(:,2), 'rs-','LineWidth',2);
semilogy(SNRdB, BER(:,3), 'k^-','LineWidth',2);
grid on;

xlabel('SNR (dB)','Interpreter','latex');
ylabel('BER','Interpreter','latex');
title('BER de um sistema OFDM (64 subportadoras, CP=16, AWGN)','Interpreter','latex');

legend('4-QAM','16-QAM','64-QAM','Location','southwest');
