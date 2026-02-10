package com.recruitment.app.controller;

import com.recruitment.app.model.Application;
import com.recruitment.app.model.Job;
import com.recruitment.app.model.User;
import com.recruitment.app.repository.ApplicationRepository;
import com.recruitment.app.repository.JobRepository;
import com.recruitment.app.service.FileStorageService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

// --- CRITICAL IMPORTS FOR PDF READING ---
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import java.io.File;
// ----------------------------------------

import java.io.IOException;
import java.nio.file.*;
import java.util.List;

@Controller
public class JobController {

    @Autowired private JobRepository jobRepository;
    @Autowired private ApplicationRepository applicationRepository;
    @Autowired private FileStorageService fileStorageService;

    public static String UPLOAD_DIRECTORY = "uploads";

    // --- 1. SHOW ALL JOBS ---
    @GetMapping("/jobs")
    public String showJobFeed(Model model, HttpSession session) {
        User user = (User) session.getAttribute("currentUser");
        model.addAttribute("user", user);
        model.addAttribute("jobs", jobRepository.findAll());
        return "job-feed";
    }

    // --- 2. SEARCH JOBS ---
    @GetMapping("/search")
    public String searchJobs(@RequestParam(value = "keyword", required = false) String keyword,
                             @RequestParam(value = "location", required = false) String location,
                             Model model, HttpSession session) {
        User user = (User) session.getAttribute("currentUser");
        model.addAttribute("user", user);

        List<Job> searchResults = jobRepository.searchJobs(keyword, location);
        model.addAttribute("jobs", searchResults);
        model.addAttribute("keyword", keyword);
        model.addAttribute("location", location);
        return "job-feed";
    }

    // --- 3. SHOW SINGLE JOB DETAILS ---
    @GetMapping("/job/{id}")
    public String showJobDetails(@PathVariable Long id, Model model, HttpSession session) {
        User user = (User) session.getAttribute("currentUser");
        model.addAttribute("user", user);

        Job job = jobRepository.findById(id).orElse(null);
        if (job == null) return "redirect:/jobs";

        model.addAttribute("job", job);
        return "job-details";
    }

    // --- 4. APPLY WITH RESUME UPLOAD ---
    @PostMapping("/apply/{jobId}")
    public String applyJob(@PathVariable Long jobId,
                           @RequestParam("resume") MultipartFile resume,
                           HttpSession session,
                           RedirectAttributes redirectAttributes) {

        User user = (User) session.getAttribute("currentUser");
        if (user == null) return "redirect:/login";

        Job job = jobRepository.findById(jobId).orElse(null);
        if (job != null) {
            Application app = new Application();
            app.setJob(job);
            app.setUser(user);
            app.setStatus("Pending");

            if (!resume.isEmpty()) {
                String fileName = fileStorageService.storeFile(resume);
                app.setResumeFileName(fileName);
            }
            applicationRepository.save(app);
            redirectAttributes.addFlashAttribute("successMessage", "Application Sent Successfully!");
        }
        return "redirect:/jobs";
    }

    // --- 5. HR: POST JOB ---
    @PostMapping("/post-job")
    public String postJob(@ModelAttribute Job job, @RequestParam("imageFile") MultipartFile file, HttpSession session) throws IOException {
        User currentUser = (User) session.getAttribute("currentUser");
        if (currentUser == null) return "redirect:/login";

        if (!file.isEmpty()) {
            String filename = System.currentTimeMillis() + "_" + file.getOriginalFilename();
            Path uploadPath = Paths.get(UPLOAD_DIRECTORY);
            if (!Files.exists(uploadPath)) Files.createDirectories(uploadPath);
            Files.copy(file.getInputStream(), uploadPath.resolve(filename), StandardCopyOption.REPLACE_EXISTING);
            job.setImage(filename);
        }
        job.setPostedBy(currentUser);
        jobRepository.save(job);
        return "redirect:/hr-profile";
    }

    // --- 6. HR: DELETE JOB ---
    @GetMapping("/delete-job/{id}")
    public String deleteJob(@PathVariable Long id, HttpSession session) {
        User currentUser = (User) session.getAttribute("currentUser");
        if (currentUser == null) return "redirect:/login";
        Job job = jobRepository.findById(id).orElse(null);
        if (job != null && job.getPostedBy().getId().equals(currentUser.getId())) {
            jobRepository.delete(job);
        }
        return "redirect:/hr-profile";
    }

    // --- 7. HR: EDIT JOB ---
    @GetMapping("/edit-job/{id}")
    public String showEditJobForm(@PathVariable Long id, Model model, HttpSession session) {
        User currentUser = (User) session.getAttribute("currentUser");
        if (currentUser == null) return "redirect:/login";
        Job job = jobRepository.findById(id).orElse(null);
        if (job != null && job.getPostedBy().getId().equals(currentUser.getId())) {
            model.addAttribute("job", job);
            return "edit-job";
        }
        return "redirect:/hr-profile";
    }

    @PostMapping("/update-job")
    public String updateJob(@ModelAttribute Job job, HttpSession session) {
        User currentUser = (User) session.getAttribute("currentUser");
        if (currentUser == null) return "redirect:/login";
        Job existingJob = jobRepository.findById(job.getId()).orElse(null);
        if (existingJob != null && existingJob.getPostedBy().getId().equals(currentUser.getId())) {
            existingJob.setTitle(job.getTitle());
            existingJob.setDescription(job.getDescription());
            existingJob.setCompanyName(job.getCompanyName());
            existingJob.setLocation(job.getLocation());
            existingJob.setSalary(job.getSalary());
            jobRepository.save(existingJob);
        }
        return "redirect:/hr-profile";
    }

    // --- 8. HR: VIEW APPLICATIONS & AI SCORE ---
    @GetMapping("/job/{id}/applications")
    public String viewApplications(@PathVariable Long id, Model model, HttpSession session) {
        User currentUser = (User) session.getAttribute("currentUser");
        if (currentUser == null) return "redirect:/login";

        Job job = jobRepository.findById(id).orElse(null);

        if (job == null || !job.getPostedBy().getId().equals(currentUser.getId())) {
            return "redirect:/hr-profile";
        }

        List<Application> applications = applicationRepository.findByJob(job);

        for (Application app : applications) {
            int score = calculateMatchScore(job, app);
            app.setTransientScore(score);

            // AUTO-REJECTION LOGIC (Adjust threshold if needed, e.g. < 30)
            if (score < 30 && "Pending".equalsIgnoreCase(app.getStatus())) {
                app.setStatus("Auto-Rejected");
                applicationRepository.save(app);
            }
        }

        model.addAttribute("job", job);
        model.addAttribute("applications", applications);
        return "view-applications";
    }

    // ==================================================================================
    //  AI SCORING METHOD (COSINE SIMILARITY VERSION)
    // ==================================================================================
    private int calculateMatchScore(Job job, Application app) {
        System.out.println(">>> DEBUG: ------------------------------------------------");
        System.out.println(">>> DEBUG: Analyzing Application for user: " + app.getUser().getUsername());

        try {
            String textToAnalyze = "";

            // 1. LOCATE THE FILE
            Path filePath = Paths.get(UPLOAD_DIRECTORY).resolve(app.getResumeFileName());
            File file = filePath.toFile();

            System.out.println(">>> DEBUG: Looking for resume at: " + file.getAbsolutePath());

            // 2. EXTRACT TEXT FROM PDF
            if (file.exists() && app.getResumeFileName().toLowerCase().endsWith(".pdf")) {
                try (PDDocument document = PDDocument.load(file)) {
                    PDFTextStripper stripper = new PDFTextStripper();
                    textToAnalyze = stripper.getText(document);
                    textToAnalyze = textToAnalyze.replaceAll("[\\n\\r]", " ");
                    System.out.println(">>> DEBUG: SUCCESS! Extracted " + textToAnalyze.length() + " characters.");
                }
            } else {
                textToAnalyze = app.getResumeFileName();
            }

            // 3. PREPARE INPUT: TITLE + DESCRIPTION + SEPARATOR + RESUME
            // This is key! We send the full Job Description so Python can compare vectors properly.
            String jobContext = job.getTitle() + " " + job.getDescription();
            String combinedInput = jobContext + "|||SEPARATOR|||" + textToAnalyze;

            // Limit length to prevent crash, but keep it substantial
            if (combinedInput.length() > 8000) {
                combinedInput = combinedInput.substring(0, 8000);
            }

            // 4. CALL PYTHON (Using Paths from your previous logs)
            String pythonPath = "C:\\Program Files\\Python314\\python.exe";
            String scriptPath = "C:\\Users\\oshan\\Desktop\\app\\app\\predict.py";

            System.out.println(">>> DEBUG: Calling Python...");
            ProcessBuilder pb = new ProcessBuilder(pythonPath, scriptPath, combinedInput);
            pb.redirectErrorStream(true);
            Process process = pb.start();

            java.io.BufferedReader reader = new java.io.BufferedReader(
                    new java.io.InputStreamReader(process.getInputStream()));

            String line = reader.readLine();
            System.out.println(">>> DEBUG: Python Score: " + line);

            // Read extra logs if Python crashes
            while(reader.ready()) {
                System.out.println(">>> DEBUG: Python Log: " + reader.readLine());
            }

            if (line != null) {
                try {
                    return Integer.parseInt(line.trim());
                } catch (NumberFormatException e) {
                    System.out.println(">>> DEBUG: Could not parse score.");
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println(">>> DEBUG: JAVA EXCEPTION: " + e.getMessage());
        }
        return 0; // Default score if something fails
    }
}