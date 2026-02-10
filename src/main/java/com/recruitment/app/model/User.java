package com.recruitment.app.model;

import jakarta.persistence.*;
import lombok.Data; // This handles the Getters/Setters automatically

@Data
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String email;
    private String password;
    private String role; // "HR" or "CANDIDATE"

    // ... inside User class ...

    // Helper: If your HTML calls "user.username", return the email or name
    public String getUsername() {
        return this.email; // or return this.fullName;
    }

// ... rest of the class ...
}