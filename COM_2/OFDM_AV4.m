clear all; close all; clc;

%% Parâmetros
Nsub  = 64;
Ncp   = 16;
SNRdB = -8:4:40;
Niter = 1e4;

Mvec = [4 16 64];   % 3 modulações
kvec = log2(Mvec);  % bits por símbolo

dataIndex  = [7:31 35:59];
pilotIndex = [32 34 60 61];
dcIndex    = 33;
Ndata = length(dataIndex);

BER = zeros(length(SNRdB),3);

%% LOOP POR SNR
for s = 1:length(SNRdB)

    SNR = SNRdB(s);

    % ---------------------------------------------------------------------
    % 1) Gerar símbolos transmitidos para as 3 modulações (vetorizado)
    % ---------------------------------------------------------------------
    dataSym_tx = zeros(Ndata, Niter, 3);
    for m = 1:3
        dataSym_tx(:,:,m) = randi([0 Mvec(m)-1], Ndata, Niter);
    end

    % ---------------------------------------------------------------------
    % 2) Modulação QAM (vetorizada por "dimensão 3")
    % ---------------------------------------------------------------------
    symbols_tx = zeros(Ndata, Niter, 3);
    for m = 1:3
        tmp = qammod(dataSym_tx(:,:,m), Mvec(m));
        tmp = tmp ./ sqrt(mean(abs(tmp(:)).^2)); % normaliza
        symbols_tx(:,:,m) = tmp;
    end

    % ---------------------------------------------------------------------
    % 3) Montagem do vetor X (64 subportadoras)
    % ---------------------------------------------------------------------
    X = zeros(Nsub, Niter, 3);
    X(dataIndex,:,:) = symbols_tx;
    X(pilotIndex,:,:) = 1;
    X(dcIndex,:,:)    = 0;

    % ---------------------------------------------------------------------
    % 4) IFFT vetorizada
    % ---------------------------------------------------------------------
    x = ifft(X, Nsub, 1);

    % ---------------------------------------------------------------------
    % 5) Adicionar CP (vetorizado)
    % ---------------------------------------------------------------------
    x_cp = [x(end-Ncp+1:end,:,:); x];

    % ---------------------------------------------------------------------
    % 6) Canal AWGN (por modulação)
    % ---------------------------------------------------------------------
    y_cp = zeros(size(x_cp));
    for m = 1:3
        % reshape ajuda awgn a aplicar corretamente
        tmp = awgn(x_cp(:,:,m), SNR, 'measured');
        y_cp(:,:,m) = tmp;
    end

    % ---------------------------------------------------------------------
    % 7) Remover CP
    % ---------------------------------------------------------------------
    y = y_cp(Ncp+1:end,:,:);

    % ---------------------------------------------------------------------
    % 8) FFT vetorizada
    % ---------------------------------------------------------------------
    Y = fft(y, Nsub, 1);

    % 9) Equalização trivial (canal = 1)
    Yeq = Y;

    % ---------------------------------------------------------------------
    % 10) Selecionar subportadoras de dados
    % ---------------------------------------------------------------------
    symbols_rx = Yeq(dataIndex,:,:);

    % Normalizar novamente
    for m = 1:3
        tmp = symbols_rx(:,:,m);
        tmp = tmp./sqrt(mean(abs(tmp(:)).^2));
        symbols_rx(:,:,m) = tmp;
    end

    % ---------------------------------------------------------------------
    % 11) Demodulação e BER
    % ---------------------------------------------------------------------
    for m = 1:3

        dataSym_rx = qamdemod(symbols_rx(:,:,m), Mvec(m));

        k = kvec(m);

        % Bits TX e RX (converter tudo de uma vez)
        bits_tx = reshape(de2bi(dataSym_tx(:,:,m), k, 'left-msb').', [], 1);
        bits_rx = reshape(de2bi(dataSym_rx      , k, 'left-msb').', [], 1);

        % BER
        BER(s,m) = sum(bits_tx ~= bits_rx) / length(bits_tx);
    end

    fprintf("SNR = %3d dB  ->  BER = [%.3e  %.3e  %.3e]\n", ...
        SNR, BER(s,1), BER(s,2), BER(s,3));

end

%% Plot
figure;
semilogy(SNRdB, BER(:,1),'bo-','LineWidth',2); hold on;
semilogy(SNRdB, BER(:,2),'rs-','LineWidth',2);
semilogy(SNRdB, BER(:,3),'k^-','LineWidth',2);
grid on;
xlabel('SNR (dB)');
ylabel('BER');
legend('4-QAM','16-QAM','64-QAM','Location','southwest');
title('BER OFDM Vetorizado – 64 subportadoras, CP=16, AWGN');
