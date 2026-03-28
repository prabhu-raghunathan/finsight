package com.finsight.transaction_service.controller;

import com.finsight.transaction_service.dto.TransactionRequest;
import com.finsight.transaction_service.dto.TransactionResponse;
import com.finsight.transaction_service.service.TransactionService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/transactions")
@RequiredArgsConstructor
public class TransactionController {

    private final TransactionService transactionService;

    @PostMapping
    public ResponseEntity<TransactionResponse> create(
            @Valid @RequestBody TransactionRequest request,
            @RequestHeader("Authorization") String authHeader) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(transactionService.create(request, authHeader));
    }

    @GetMapping
    public ResponseEntity<List<TransactionResponse>> getAll(
            @RequestHeader("Authorization") String authHeader) {
        return ResponseEntity.ok(transactionService.getAllForUser(authHeader));
    }

    @GetMapping("/{id}")
    public ResponseEntity<TransactionResponse> getById(
            @PathVariable Long id,
            @RequestHeader("Authorization") String authHeader) {
        return ResponseEntity.ok(transactionService.getById(id, authHeader));
    }

    @PutMapping("/{id}")
    public ResponseEntity<TransactionResponse> update(
            @PathVariable Long id,
            @Valid @RequestBody TransactionRequest request,
            @RequestHeader("Authorization") String authHeader) {
        return ResponseEntity.ok(transactionService.update(id, request, authHeader));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(
            @PathVariable Long id,
            @RequestHeader("Authorization") String authHeader) {
        transactionService.delete(id, authHeader);
        return ResponseEntity.noContent().build();
    }
}