package com.finsight.transaction_service.service;

import com.finsight.transaction_service.dto.TransactionRequest;
import com.finsight.transaction_service.dto.TransactionResponse;
import com.finsight.transaction_service.entity.Transaction;
import com.finsight.transaction_service.repository.TransactionRepository;
import com.finsight.transaction_service.security.JwtUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class TransactionService {

    private final TransactionRepository transactionRepository;
    private final JwtUtil jwtUtil;

    private Long extractUserId(String authHeader) {
        String token = authHeader.substring(7);
        String email = jwtUtil.extractEmail(token);
        // We use email hashCode as userId for now
        // In production this would be a call to User Service
        return (long) email.hashCode();
    }

    private TransactionResponse toResponse(Transaction t) {
        return TransactionResponse.builder()
                .id(t.getId())
                .userId(t.getUserId())
                .amount(t.getAmount())
                .type(t.getType())
                .category(t.getCategory())
                .description(t.getDescription())
                .transactionDate(t.getTransactionDate())
                .createdAt(t.getCreatedAt())
                .build();
    }

    public TransactionResponse create(TransactionRequest request, String authHeader) {
        Long userId = extractUserId(authHeader);

        Transaction transaction = Transaction.builder()
                .userId(userId)
                .amount(request.getAmount())
                .type(request.getType())
                .category(request.getCategory())
                .description(request.getDescription())
                .transactionDate(request.getTransactionDate())
                .build();

        return toResponse(transactionRepository.save(transaction));
    }

    public List<TransactionResponse> getAllForUser(String authHeader) {
        Long userId = extractUserId(authHeader);
        return transactionRepository.findByUserId(userId)
                .stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
    }

    public TransactionResponse getById(Long id, String authHeader) {
        Long userId = extractUserId(authHeader);
        Transaction transaction = transactionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Transaction not found"));

        if (!transaction.getUserId().equals(userId)) {
            throw new RuntimeException("Unauthorized");
        }

        return toResponse(transaction);
    }

    public TransactionResponse update(Long id, TransactionRequest request, String authHeader) {
        Long userId = extractUserId(authHeader);
        Transaction transaction = transactionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Transaction not found"));

        if (!transaction.getUserId().equals(userId)) {
            throw new RuntimeException("Unauthorized");
        }

        transaction.setAmount(request.getAmount());
        transaction.setType(request.getType());
        transaction.setCategory(request.getCategory());
        transaction.setDescription(request.getDescription());
        transaction.setTransactionDate(request.getTransactionDate());

        return toResponse(transactionRepository.save(transaction));
    }

    public void delete(Long id, String authHeader) {
        Long userId = extractUserId(authHeader);
        Transaction transaction = transactionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Transaction not found"));

        if (!transaction.getUserId().equals(userId)) {
            throw new RuntimeException("Unauthorized");
        }

        transactionRepository.delete(transaction);
    }
}