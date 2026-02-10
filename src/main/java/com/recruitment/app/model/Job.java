package com.recruitment.app.model;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDate;

@Data
@Entity
@Table(name = "jobs")
public class Job {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;
    @Column(length = 5000) // Allow longer text
    private String description;
    private String location;
    private String salary;
    private String companyName;
    private LocalDate postedDate;

    // NEW: Stores the filename of the uploaded image
    private String image;

    @ManyToOne
    @JoinColumn(name = "posted_by_user_id")
    private User postedBy;

    @PrePersist
    protected void onCreate() {
        postedDate = LocalDate.now();
    }

    // ... inside the class ...

    private String jobType; // e.g., "Full Time", "Remote"

    // Add Getter and Setter
    public String getJobType() { return jobType; }
    public void setJobType(String jobType) { this.jobType = jobType; }

// ... rest of the class ...
}